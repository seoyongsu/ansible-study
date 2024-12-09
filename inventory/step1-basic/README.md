# Step1 : Basic Inventory


목표 : 기본 인벤토리 연습

## 기본 명령어 확인
```
ansible-inventory --help
```
자주 사용 되는 옵션
* `-i` 인벤토리 파일 : 입력이 없으면 `ansible.cfg`에 구성된 경로로 설정됨


아래표에 대한 인벤토리를 생성

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

## 1. ini 방식
`vi inventory` or `vi inventory.ini` 


```ini
172.17.0.2
default1 ansible_host=172.17.0.3
default2 ansible_host=172.17.0.4 ansible_user=root

[webservers]
172.17.0.5
web1 ansible_host=172.17.0.6
web2 ansible_host=172.17.0.7 ansible_user=root

[dbservers]
172.17.0.8
db2 ansible_host=172.17.0.9

[dbservers:vars]
ansible_user=db_user
ansible_password=db_userpass
```




## 2. yaml 방식

```
vi inventory.yaml
```

```yaml
all:
  hosts:
    172:0.0.2:
    default1:
      ansible_host: 172.0.0.3
    default2:
      ansible_host:
        - 172.0.0.4
        
        
  children:
    webservers:
      hosts:
        172.17.0.5:
        web1:
          ansible_host: 172.17.0.6
        web2:
          ansible_host: 172.17.0.7
          ansible_user: root

    dbservers:
      hosts:
        172.0.0.8:
        db2:
          ansible_host: 172.17.0.9

      vars:
        ansible_user: db_user
        ansible_password: db_userpass
```


## 3. 확인
```
ansible-inventory -i [inventory file] --list
```

```
{
    "_meta": {
        "hostvars": {
            "172.17.0.8": {
                "ansible_password": "db_userpass",
                "ansible_user": "db_user"
            },
            "db2": {
                "ansible_host": "172.17.0.9",
                "ansible_password": "db_userpass",
                "ansible_user": "db_user"
            },
            "default1": {
                "ansible_host": "172.17.0.3"
            },
            "default2": {
                "ansible_host": "172.17.0.4",
                "ansible_user": "root"
            },
            "web1": {
                "ansible_host": "172.17.0.6"
            },
            "web2": {
                "ansible_host": "172.17.0.7",
                "ansible_user": "root"
            }
        }
    },
    "all": {
        "children": [
            "ungrouped",
            "webservers",
            "dbservers"
        ]
    },
    "dbservers": {
        "hosts": [
            "172.17.0.8",
            "db2"
        ]
    },
    "ungrouped": {
        "hosts": [
            "172.17.0.2",
            "default1",
            "default2"
        ]
    },
    "webservers": {
        "hosts": [
            "172.17.0.5",
            "web1",
            "web2"
        ]
    }
}
```