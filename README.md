# ansible-study

## 앤서블 이란?

앤서블은 IT 자동화 도구로, 서버 관리, 애플리케이션 배포, 설정 관리(Configuration Management), 프로비저닝(Provisioning)을 쉽게 할 수 있도록 돕는 도구입니다.

에이전트가 필요 없는(agentless) 구조로 설계되어, 단순함과 확장성을 특징으로 합니다.

앤서블의 주요 목표는 단순성과 사용 편의성입니다. 최소한의 변경만 이용하고, 데이터 전송을 위해서 OpenSSH를 이용합니다.
사람이 이해하기 편하도록 yaml 언어를 이용하여 작업합니다.

앤서블의 단순성은 개발자, 시스템 관리자, 릴리스 엔진니어, IT 관리자 등 많은 영역의 사람들이 작업할 수 있도록 지원합니다.
앤서블은 작은 인스턴스의 설정 부터 수천 개의 인스턴스가 있는 엔터프라이즈 환경까지 모든 환경을 관리할 수 있습니다.

앤서블은 에이전트가 없이  SSH 연결을 이용해서 머신을 관리합니다. OpenSSH를 이용하기 대문에 보안에도 우수합니다.



## 개념 및 용어
### • 제어 노드 (Control Node)
* Ansible을 실행하는 중앙 관리 서버를 Control Node 라고 합니다.
* 명령을 통해 Manged Node를 관리 합니다.
* Playbook의 작성 및 실행 이루어 집니다.

### • 매니지드 노드 (Managed Node)
* Ansible이 관리하는 대상 서버를 Managed Node 라고 합니다
* SSH를 통해 접근하며, 별도에 에이전트가 필요 없습니다.

### • 인벤토리 (Inventory)
* Ansible이 관리할 서버(Managed Node)의 목록과 설정을 관리 합니다
* 호스트 파일이라고도 하며, Managed Node의 IP 주소, 호스트 정보, 변수 등과 같은 정보를 갖고 있습니다.
* 작성 방법에는 `ini` or `yaml` 등과 같이 작성 가능합니다.


### • 플레이북 (Playbook)
* 작업 절차와 구성을 정의하는 `YAML` 파일
* 절차형 방식으로 실행
```
- name: Install and start nginx
  hosts: web_servers
  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
    - name: Start nginx service
      service:
        name: nginx
        state: started
```

### • 테스크 (Task)
* Tasks는 Playbook에서 하나의 작업 단위를 의미합니다.
* 특정 모듈을 호출하여 작업을 수행할 수 있습니다.
* 작업은 순차적으로 실행되며, 조건이나 핸들러 등을 활용해 유연하게 동작할 수 있습니다.
```
tasks:
  - name: Install nginx
    apt:
      name: nginx
      state: latest
```

### • 모듈 (Module)
* 모듈은 특정 작업을 수행하는 Ansible의 기능 단위입니다.
* 모듈은 단일 명령어 이자 수행할 작업입니다. `cp`, `apt`, `wget` 등의 단일 명령어가 모듈이라고 할 수 있습니다.
* 패키지 설치, 파일 복사, 서비스 시작 등 다양한 작업을 모듈로 구성하여 재사용성을 높일 수 있습니다.

### • 핸들러 (Handler)
* 특정 조건이 발생했을 때 실행되는 태스크입니다.
* 주로 서비스의 상태 변경 시 재시작 등을 처리할 때 사용됩니다.
* 핸들러는 태스크에서 notify로 호출됩니다.



## 참고 문헌
* https://wikidocs.net/book/6350