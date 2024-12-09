# Step2 : Dynamic Inventory

목표 : Ansible 인벤토리를 동적으로 구성 연습 보기

what? : 만약 관리 해야 하는 Managed Node(호스트) 정보가 수백개 수천개 가 된다고 하면, 계속 정적으로 작성되어 있는 `inventory`
파일을 관리해야하며, 비효율 발생

Ansible에서는 다양한 플러그인이 존재 하며 응용해서 관리 가능함.


* [가이드 문서-1](https://docs.ansible.com/ansible/latest/inventory_guide/intro_dynamic_inventory.html)
* [가이드 문서-2](https://docs.ansible.com/ansible/latest/reference_appendices/python_3_support.html)


## Json Inventory 검증
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


## 결과
JSON의 결과만 동적으로 구성 하면 수백, 수천개의 호스트 정보를 쉽게 관리 가능 









