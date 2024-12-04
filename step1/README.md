# Step1

목표 : Managed Node에 Nginx를 설치 및 실행

**준비물**
* Control Node
```
docker run -d -it --name control-node ubuntu
```

* Managed Node (2)
```
docker run -d -it --name managed-node-1 -p 8081:80 -p 2221:22 ubuntu
docker run -d -it --name managed-node-2 -p 8082:80 -p 2222:22 ubuntu
```
| Docker Container name | IP         | Http Port  | ssh port   | 
|-----------------------|------------|------------|------------|
| managed-node-1        | 172.17.0.3 | 80 -> 8081 | 22 -> 2221 |
| managed-node-2        | 172.17.0.4 | 80 -> 8082 | 22 -> 2222 |

참고 : [실습 환경 구성](../Tutorial-Environment.md)


## Inventory
* Managed Node 목록 작성

`vi inventory`
```
[webserver]
172.17.0.2
172.17.0.3

[webserver:vars]
ansible_user=root
```

**inventory file 확인**
```
ansible -i inventory --list
```

**Ping 테스트**
```
ansible -i inventory -m ping webserver
```
* `inventory`에 SSH 인증 정보가 없기 때문에 `Connection Fail` or `Permission denied` 가 발생
```
ansible -i inventory -m ping -k webserver
```
* `-k` 옵션으로 직접 비밀번호 입력 하는 방식으로 ping 체크

**결과**
```
172.17.0.2 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
172.17.0.3 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
```

## Playbook
* Nginx 설치 & 실행하는 playbook 구성
    * nginx install : nginx 설치
    * nginx start : nginx 실행

`vi playbook-nginx.yaml`
```
---
- name: webserver nginx install & start
  hosts: webserver
  tasks:
    # Nginx 설치
    - name: Nginx install
      apt:
        name: nginx
        state: present
        
    # Nginx service start를 위해 설치
    - name: SystemCtl install
      apt:
        name: systemctl
        state: present
        
    # Nginx 데몬 실행
    - name: Nginx start
      service:
        name: nginx
        state: started

```

**playbook check**
```
ansible-playbook -i inventory playbook-nginx-install.yaml --syntax-check
ansible-playbook -i invenroty playbook-nginx-install.yaml --check
```


## Playbook 실행
```
ansible-playbook -i inventory playbook-nginx-install.yaml
```
* 인증 오류가 발생하면 `-k` 옵션으로 직접 로그인 시도!

**Playbook 실행 결과 예시**
```
PLAY [webserver nginx install & start] *********************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [172.17.0.4]
ok: [172.17.0.3]

TASK [Nginx install] ***************************************************************************************************
ok: [172.17.0.3]
changed: [172.17.0.4]

TASK [SystemCtl install] ***********************************************************************************************
ok: [172.17.0.3]
changed: [172.17.0.4]

TASK [Nginx start] *****************************************************************************************************
ok: [172.17.0.3]
changed: [172.17.0.4]

PLAY RECAP *************************************************************************************************************
172.17.0.3                 : ok=4    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
172.17.0.4                 : ok=4    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

```








