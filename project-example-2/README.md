# Step2

목표 : Managed Node SSH key 배포

**준비물**
* Managed Node
```shell
docker run -d -it --name managed-node ubuntu
```
참고 : [실습 환경 구성](../Tutorial-Environment/README.md)


## SSH key 생성
* ansible 서버(Control-Node) 에서 실행
```shell
ssh-keygen -b 2048 -t rsa -f ~/.ssh/ansible_key -q -N ''
```

## Ansible.cfg
* private key 설정
* host_key_checking False : 예제에서는 ssh key 배포를 위해 pw 방식으로 인증
```
[defaults]
private_key_file = ~/.ssh/ansible_key
host_key_checking = False
```

## play book
* play book 작성
``` yaml
---
- name: ssh play book
  hosts: '{{ target_host | default("all") }}'
  gather_facts: no
  tasks:
    - name: push ansible pub key
      authorized_key:
        user: "{{ ansible_user | default('root')}}"
        state: present
        key: "{{ lookup('file', item) }}"
      with_items:
        - '~/.ssh/ansible_key.pub'
```

* play book 실행
``` shell
$ ansible-playbook -i inventory ssh.yml -k
SSH password:

PLAY [deploy ssh public key] ********************************************************************************************************************************************************************************************************************************

TASK [ssh : push ansible pub key] ***************************************************************************************************************************************************************************************************************************
changed: [172.17.0.2]

PLAY RECAP **************************************************************************************************************************************************************************************************************************************************
172.17.0.2                 : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```


## 확인
1) Managed node 접속 하여 `authorized_keys` 파일 생성 확인
```shell
$ cd ~/.ssh
$ ls
authorized_keys
```

2) Ansible ping으로 테스트
```shell
$ ansible -i inventory -m ping all
172.17.0.2 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
```