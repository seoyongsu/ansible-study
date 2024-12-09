# Step2 : Dynamic Inventory

목표 : Ansible 인벤토리 방식으로 Mysql과 연동해서 동적으로 구성 연습  
해당 예제에서는 python으로 DB 조회후 Inventory(Json) 목록을 추출!  


what? : 만약 관리 해야 하는 Managed Node(호스트) 정보가 수백개 수천개 가 된다고 하면, 계속 정적으로 작성되어 있는 `inventory`
파일을 관리해야하며, 비효율 발생

Ansible에서는 다양한 플러그인이 존재 하며 응용해서 관리 가능함.



| ip         | group           | hostname | vars        |
|------------|-----------------|----------|-------------|
| 172.17.0.2 | None(Ungrouped) |          |             |
| 172.17.0.3 | None(Ungrouped) | default1 |             |
| 172.17.0.4 | None(Ungrouped) | default2 | O           |
| 172.17.0.5 | webservers      |          |             |
| 172.17.0.6 | webservers      | web1     |             |
| 172.17.0.7 | webservers      | web2     | O           |
| 172.17.0.8 | dbservers       |          | O (공통으로 관리) |
| 172.17.0.9 | dbservers       | db2      | O (공통으로 관리) |

**사전 준비**

* hosts : 호스트(Managed Node)
```SQL
CREATE TABLE hosts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ip VARCHAR(15) NOT NULL,
    host_name VARCHAR(255),
    group_name VARCHAR(255)
);

INSERT INTO hosts(ip, host_name, group_name)
VALUES
    ('172.17.0.2', 	NULL, 		null),
    ('172.17.0.3', 	'default1', 	NULL),
    ('172.17.0.4', 	'default2', 	NULL),
    ('172.17.0.5', 	NULL, 		'webservers'),
    ('172.17.0.6', 	'web1', 	'webservers'),
    ('172.17.0.7', 	'web2', 	'webservers'),
    ('172.17.0.8', 	NULL, 		'dbservers'),
    ('172.17.0.9', 	'db2', 		'dbservers');
```


* hosts_vars : 호스트의 vars
```SQL
create table hosts_vars(
    ip VARCHAR(15) NOT NULL,
    `keys` VARCHAR(255),
    `VALUES` VARCHAR(255),

    INDEX IDX_01 (ip)
);

INSERT INTO hosts_vars(ip, `keys`, `values`)
VALUES
    ('172.17.0.4', 'ansible_user', 'root'),
    ('172.17.0.7', 'ansible_user', 'root'),
    ('172.17.0.7', 'ansible_password', '1234');
```


* hosts_group_vars : 호스트 그룹의 vars

```SQL
create table hosts_group_vars(
    group_name VARCHAR(255) default 'ALL',
    `keys` VARCHAR(255),
    `values` VARCHAR(255),

    INDEX IDX_01 (group_name)
);

INSERT INTO hosts_group_vars(group_name, `keys`, `values`)
VALUES
    ('dbservers', 'ansible_user','root'),
    ('dbservers', 'ansible_password','db_userpass');
```



### 1-1 Python으로 Inventory json 추출 스크립트 작성
Python 플러그인
* json : DB 조회 정보를 Json 으로 반환
* mysql: mysql Connect
```python
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

```





