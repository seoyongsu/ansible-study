# inventory

Ansible이 관리 하는 서버(Managed Node)의 목록과 설정을 갖고 있는 파일을 인벤토리라고 합니다.
인벤토리는 Manged Node를 정의하고 그룹을 사용하여 여러 호스트에서 동시에 자동화 작업을 실행할 수 있습니다.
`ini` 또는 `yaml` 방식으로 인벤토리를 관리 할 수 있습니다.


# Basic - Inventory
* [가이드 문서](https://docs.ansible.com/ansible/latest/inventory_guide/intro_inventory.html)



# Dynamic - Inventory
* [가이드 문서-1](https://docs.ansible.com/ansible/latest/inventory_guide/intro_dynamic_inventory.html)
* [가이드 문서-2](https://docs.ansible.com/ansible/latest/reference_appendices/python_3_support.html)


### Json Inventory Test
* CSV, DB, Plug In 등을 활용해서 동적 인벤토리 구성 가능 함
* 검증을 위해 `JSON` 파일로 테스트

`vi test.json`
```JSON
{
  "all": {
    "hosts": {
      "172:0.0.1": {},
      "default1": {
        "ansible_host": "172.0.0.3"
      },
      "default2": {
        "ansible_host": [
          "172.0.0.4"
        ]
      }
    },
    "children": {
      "webservers": {
        "hosts": {
          "172.17.0.5": {},
          "web1": {
            "ansible_host": "172.17.0.6"
          },
          "web2": {
            "ansible_host": "172.17.0.7",
            "ansible_user": "root",
            "ansible_password": "1234"
          }
        }
      },
      "dbservers": {
        "hosts": {
          "172.0.0.8": {},
          "db2": {
            "ansible_host": "172.17.0.9"
          }
        },
        "vars": {
          "ansible_user": "db_user",
          "ansible_password": "db_userpass"
        }
      }
    }
  }
}
```
```
ansible-inventory test.json --list
```

