# Tutorial Environment
Docker 이용한 튜토리얼 기본 환경 구성 방법



## Docker
**Docker Container 생성**
```
docker run -d -it --name [container name] ubuntu
```
* 필요에 따라 `-p 8081:80 -p 2221:22` 와 같은 방식으로 포트 포워딩

**Docker Container 접속**
```
docker exec -it [container name] /bin/bash
```



## Managed Node
**Open SSH Server 설치**
```
apt update
apt install openssh-server
```

**sshd_config 설정**
* 문서 편집 도구가 없는 경우 `apt install vim` 명령을 통해 편집 도구 설치
```
vi /etc/ssh/sshd_config
```
```
#Port 22 (as_is)
Port 22 (to_be)
...
...
#PermitRootLogin prohibit-password (as_is)
PermitRootLogin yes (to_be)
```
* port 주석 제거
* ROOT 계정 로그인 허용으로 설정


**Root PW 변경**
```
passwd
```

**SSH Config 적용을 위해 재시작**
```
service ssh restart
```

## Control Node
**Ansible 설치**
* OS 환경에 맞는 설치 방법은 [설치 가이드](install/Install) 문서 참고
```
apt update
apt install ansible
```


**문서 편집을 위해 편집 도구 설치**
```
apt install vim
```


**앤서블 설치 확인**
```
ansible --version
```
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