#!/usr/bin/env python3

import json

import pymysql
import pymysql.cursors

# DB Config Option
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "1234",
    "database": "test",
    "port": 3306,  # 기본 MySQL 포트
}


# Inventory data select Query
def fetch_inventory_data():
    query = """
        select 
            m.ip,
            m.host_name,
            m.group_name,
            ( 
                SELECT JSON_OBJECTAGG( `keys`,`values`) FROM hosts_vars a WHERE m.ip = a.ip GROUP BY a.ip
            ) as vars
        from
            hosts m
    """
    return execute_query(query, DB_CONFIG)


# Inventory Group Vars select Query
def fetch_inventory_group_vars_data():
    query = """
    SELECT
        group_name,
        JSON_OBJECTAGG( `keys`,`values`) AS vars 
    FROM
        hosts_group_vars.sql 
    GROUP BY group_name
    """

    return execute_query(query, DB_CONFIG)


# DB Query Execute
def execute_query(query, db_config):
    connection = None
    cursor = None
    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(f"Data Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# generata inventory
def generate_inventory(hosts_data, group_vars):
    # inventory default json format
    inventory_format = {
        "all": {
            "hosts": {},
            "children": {
            }
        }
    }

    # Json Basic Inventory
    for host in hosts_data:
        ip = host['ip']
        host_name = host["host_name"]
        group_name = host["group_name"]
        host_vars = host.get('vars', None)

        # host_name == null  -> {}
        # host_name not null -> {'ansible_host': ip}
        var = {} if host_name is None else {'ansible_host': ip}
        if host_vars is not None:
            var.update(json.loads(host_vars))

        # group_name == null
        if group_name is None:
            if host_name is None:
                inventory_format['all']['hosts'][ip] = var
            else:
                inventory_format['all']['hosts'][host_name] = var
        # group_name not null
        else:
            if group_name not in inventory_format['all']['children']:
                inventory_format['all']['children'][group_name] = {'hosts': {}}
            if host_name is not None:
                inventory_format['all']['children'][group_name]['hosts'][host_name] = var
            else:
                inventory_format['all']['children'][group_name]['hosts'][ip] = var

    # add inventory group vars
    for group_var in group_vars:
        group_name = group_var["group_name"]
        var = json.loads(group_var['vars'])
        if group_name is None or group_name == '' or group_name == 'ALL':
            inventory_format['all']['vars'] = var
        else:
            inventory_format['all']['children'][group_name]['vars'] = var

    return inventory_format


if __name__ == "__main__":
    data = fetch_inventory_data()
    group_vars = fetch_inventory_group_vars_data()
    inventory = generate_inventory(data, group_vars)
    print(json.dumps(inventory, indent=4))
