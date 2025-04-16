import argparse
import sys
from datetime import datetime

import pymysql
import requests
import yaml
import csv


class AWXClient:
   """
   AWX Client class
   """
   __TOKEN = None  # AWX Token

   def __init__(self, host='localhost', token=None, username='', password='password'):
      self._base_url = f'http://{host}/api/v2'  # AWX BASE URL
      if token:
         self.__class__.__TOKEN = token
      else:
         self._username = username
         self._password = password
         self.__class__.__TOKEN = self.__authenticate()

   def __authenticate(self):
      """
      AWX 인증 토큰을 받아 오는 함수
      :return:
      """
      response = requests.post(
         f"{self._base_url}/tokens/",  # AWX 토큰 엔드포인트
         auth=(self._username, self._password),
         timeout=5
      )
      if response.status_code == 201:
         return response.json().get('token')
      else:
         raise Exception(f"AWX 토큰 발급 실패: {response.status_code} - {response.text}")

   def __execute_api(self, method, end_point, body=None, params=None):
      """
      API 호출 하는 공통 함수
      """
      url = f"{self._base_url}{end_point}/"
      headers = {
         'Authorization': f"Bearer {self.__TOKEN}",
         'Content-Type': 'application/json'
      }
      response = requests.request(method=method, url=url, headers=headers, json=body, params=params, verify=False,
                                  timeout=5)

      if 200 <= response.status_code < 300:
         try:
            return response.json()  # JSON 응답이 있으면 반환
         except ValueError:
            return None  # JSON 디코딩이 실패하면 None 반환
      else:
         print(f" API {method} {url}  실패: {response.status_code}, 응답: {response.text}")
         return None

   def get_inventory(self, name=None):
      inventories = self.__execute_api("GET", "/inventories", params={"name": name})
      if inventories and inventories['count'] > 0:
         return inventories['results'][0]  # 첫 번째 결과 반환
      return None

   def create_inventory(self, name=None, inventory_vars: yaml = None, override: bool = True):
      """
      AWX의 inventory를 생성 하는 함수
      :param name:            인베토리 이름
      :param inventory_vars:  인벤토리의 vars
      :param override:        무시하고 생성 여부 스냅샷으로 기존것 이름 변경됨
      :return:
      """
      inventory = self.get_inventory(name)

      ## override false : 기존 인벤토리 이름 변경 후 새로 생성
      if inventory and not override:
         inventory_id = inventory['id']
         snap_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
         snap_name = f"{name} [Snap_Shot : {snap_time}]"
         self.__execute_api("PATCH", f"/inventories/{inventory_id}", body={'name': snap_name})
         return self.create_inventory(name, inventory_vars, override)

      ## inventory_vars 값이 있으면 update
      if inventory and override:
         if inventory_vars:
            return self.__execute_api(
               "PATCH",
               f"/inventories/{inventory['id']}",
               body={'variables': inventory_vars}
            )
         return inventory

      ## 인벤토리가 없을 경우 새로 생성
      body = {
         'name': name,
         'organization': 1,
         'variables': inventory_vars,
      }
      return self.__execute_api("POST", "/inventories", body=body)

   def get_host(self, name, inventory=None):
      params = {"name": name}
      if inventory is not None:
         params["inventory"] = inventory['id']
      hosts = self.__execute_api(method="GET", end_point='/hosts', params=params)
      if hosts and hosts['count'] > 0:
         return hosts['results'][0]  # 첫 번째 결과 반환
      return None

   def create_inventory_host(self, inventory, name, host_vars: yaml = None, override: bool = True):
      """
      Inventory에 Host 정보를 생성 하는 함수
      :param inventory_id:
      :param host_name:
      :param host_vars:
      :return:
      """
      host = self.get_host(name, inventory=inventory)
      if host:
         if override:
            host_id = host['id']
            body = {'variables': host_vars}
            return self.__execute_api(method="PATCH", end_point=f'/hosts/{host_id}', body=body)
         return host
      else:
         inventory_id = inventory['id']
         body = {
            'name': name,
            'description': '',
            'inventory': inventory_id,
            'enabled': True,
            'instance_id': None,
            'variables': host_vars
         }
         return self.__execute_api(method="POST", end_point='/hosts', body=body)

   def create_inventory_group(self, inventory, name, group_vars: yaml = None):
      """
      AWX의 Inventory의 group을 생성 하는 함수
      :param inventory:
      :param name: 그룹명
      :param group_vars: 그룹의 vars
      :return: group ID
      """
      inventory_id = inventory['id']

      group = self.__execute_api("GET", "/groups", params={"inventory": inventory_id, "name": name})
      if group and group['count'] > 0:
         return group['results'][0]
      else:
         body = {
            'name': name,
            'description': "",
            'inventory': inventory_id,
            'variables': group_vars
         }
         return self.__execute_api("POST", "/groups", body=body)

   def add_host_to_group(self, group: dict, host: dict):
      """
      inventory host 및 group 연결
      :param host:
      :param group:
      :param group_id:
      :param host_id:
      :return:
      """
      if all((host, group)):
         group_id = group['id']
         host_id = host['id']
         self.__execute_api(method="POST", end_point=f'/groups/{group_id}/hosts', body={"id": host_id})



class Load_Csv:
   @staticmethod
   def get_inventories(csv_file):
      try:
         with open(csv_file, newline='', encoding='utf-8-sig') as file:
            return list(csv.DictReader(file))
      except FileNotFoundError:
         print(f"[ERROR] Csv file not found: {csv_file}")
         sys.exit(1)
      except Exception as e:
         print(f"[ERROR] Load CSV Exception: {e}")
         sys.exit(1)

class Load_DB:
   @staticmethod
   def execute(*, host=None, user=None, password='', database=None, port=3306, query=None):
      db_config = {
         "host": host,
         "user": user,
         "password": password,
         "database": database,
         "port": port,  # 기본 MySQL 포트
      }
      try:
         with pymysql.connect(**db_config) as conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
               cursor.execute(query)
               return cursor.fetchall()
      except pymysql.MySQLError as err:
         print(f"MySQL Error: {err}")
         return None



if __name__ == '__main__':

   # sys.argv.extend([
   #    '--awx_host', '172.19.165.43:32576',
   #    '--awx_token', 'KWxhsGkmzBcxxJt6RgUxS5wFKONysx',
   #    '--csv_file', 'inventories.csv',
   #    # '--make_type', '',
   #    # '--include_pending', 'Yes',
   #    '--override', 'yes'
   # ])

   parser = argparse.ArgumentParser()
   parser.add_argument('--awx_host', required=True, help="AWX host")
   parser.add_argument('--awx_token', help="Token-based authentication")
   parser.add_argument('--awx_user', help="Username for AWX")
   parser.add_argument('--awx_password', help="Password for AWX")
   parser.add_argument('--override', help="Inventories Override (yes/no) ? (default: yes)")
   parser.add_argument('--make_type', required=True, help='CSV, DB')
   ##
   make_types = ['CSV', 'DB']
   ## Make Type CSV
   parser.add_argument('--csv_file', help="CSV File")

   ## Make Type DB
   parser.add_argument('--db_host', help="DB Host")
   parser.add_argument('--db_user', help='DB User')
   parser.add_argument('--db_password', help='DB PASSWORD')
   parser.add_argument('--db_port', help='DB PORT', default='3306')
   parser.add_argument('--db_name', help="Data Base Name")
   parser.add_argument('--db_query', help='Inventories Select Query')

   args = parser.parse_args()

   ### 아규먼트 검증
   ## 1.AWX 인증 값 검증
   if not args.awx_token:
      if not args.awx_user or not args.awx_password:
         print("ERROR: Either --awx_token OR both --awx_user and --awx_password are required.", file=sys.stderr)
         sys.exit(1)

   ## 2. Make Type 검증 및 설정
   inventories_items = []
   if args.make_type not in make_types:
      print("ERROR: Either --make_type [CSV, DB, JSON]", file=sys.stderr)
      sys.exit(1)
   ## 2-1 CSV
   if args.make_type == 'CSV':
      if not args.csv_file:
         print("[ERROR] Either --csv_file",  file=sys.stderr)
         sys.exit(1)
      inventories_items = Load_Csv(csv_file=args.csv_file)

   ## 2-2 DB
   elif args.make_type == 'DB':
      if not args.db_host:
         print("[ERROR] Either --db_host",  file=sys.stderr)
         sys.exit(1)
      if not args.db_user:
         print("[ERROR] Either --db_user",  file=sys.stderr)
         sys.exit(1)
      if not args.db_password:
         print("[ERROR] Either --db_password",  file=sys.stderr)
         sys.exit(1)
      if not args.db_port:
         print("[ERROR] Either --db_port",  file=sys.stderr)
         sys.exit(1)
      if not args.db_name:
         print("[ERROR] Either --db_name",  file=sys.stderr)
         sys.exit(1)
      if not args.db_query:
         print("[ERROR] Either --db_query",  file=sys.stderr)
         sys.exit(1)

      inventories_items = Load_DB(host=args.db_host, user=args.db_user, password=args.db_password,
                            database=args.db_name, port=args.db_port, query=args.db_query)

   ## 3. 인벤토리 덮어쓰기 옵션
   override = args.override in ['true', '1', 'yes'] if args.override else True


   ## TODO...Data parser   Your Inventories
   ## Example

   ## 1. Make AWX New Inventory
   awx = AWXClient(host=args.awx_host, token=args.awx_token, username=args.awx_user, password=args.awx_password)
   inventory = awx.create_inventory('Hello World', override=True)

   ## 2. Inventory Add Hosts
   for item in inventories_items:
      host_name = item.get('host_name')
      ansible_host = item.get('ansible_host')
      ansible_port = item.get('ansible_port')
      ansible_user = item.get('ansible_user')

      host_vars = {}
      if ansible_host:
         host_vars['ansible_host'] = ansible_host
      if ansible_port:
         host_vars['ansible_port'] = int(ansible_port)
      if ansible_user:
         host_vars['ansible_user'] = ansible_user

      # Host 추가
      host = awx.create_inventory_host(inventory=inventory, name=host_name, host_vars=yaml.dump(host_vars))
