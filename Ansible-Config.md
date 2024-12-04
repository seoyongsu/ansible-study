# Ansible Config


[공식 문서](https://docs.ansible.com/ansible/latest/reference_appendices/config.html)

* forks: 한번에 처리하는 노드의 개수.
* host_key_checking: 앤서블에 연결하는 호스트의 키 확인 여부
* remote_user: 서버에 접속하는 유저명
* remote_port: 서버에 접속하는 SSH 포트
```
[defaults]
forks = 50 
host_key_checking = False
remote_user = deploy
remote_port = 22
```

## Config file 설정
* Ansible Config는 `ansible.cfg` 파일을 통해 관리됨


`ansible --version`
```
ansible [core 2.16.3]
  config file = None
  configured module search path = ['/root/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python3/dist-packages/ansible
  ansible collection location = /root/.ansible/collections:/usr/share/ansible/collections
  executable location = /usr/bin/ansible
  python version = 3.12.3 (main, Nov  6 2024, 18:32:19) [GCC 13.2.0] (/usr/bin/python3)
  jinja version = 3.1.2
  libyaml = True
```
* 위와 같이 `config file` 경로가 `None` 인 경우 아래와 같은 방법으로 Config 설정 가능함


```
vi ansible.cfg
```
```
[defaults]
inventory = /path/to/your/inventory
or
inventory = /path/to/your/inventory.yaml
```


`ansible --version` 명령을 통해 확인
```
ansible [core 2.16.3]
  config file = /path/to/your/ansible.cfg
  configured module search path = ['/root/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python3/dist-packages/ansible
  ansible collection location = /root/.ansible/collections:/usr/share/ansible/collections
  executable location = /usr/bin/ansible
  python version = 3.12.3 (main, Nov  6 2024, 18:32:19) [GCC 13.2.0] (/usr/bin/python3)
  jinja version = 3.1.2
  libyaml = True
```


```
[defaults]
forks = 50 
host_key_checking = False
remote_user = deploy
remote_port = 22
```
