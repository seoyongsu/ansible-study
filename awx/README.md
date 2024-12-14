# AWX
AWX는 Ansible 위에 구축된 웹 기반 사용자 인터페이스, REST API 및 작업 환경을 제공 하는 도구 입니다.


| AWX Version | Environment |
|-------------|-------------|
| &ge; 18.0.0 | Kubernetes  |
| &le; 17.1.0 | Docker      |
* AWX는 18 버전을 기준으로 이전 버전의 Docker 지원과 이후 k3s(Lightweight Kubernetes) 지원으로 나뉩니다.

* GitHub : https://github.com/ansible/awx
---

## Ansible AWX &le; 17.1.0 Install
Ansible AWX의 `17.1.0` 이전 버전은 Docker 환경을 지원함

**필수 패키지**
* Ansible
* Docker
* Python

### 1. AWX Download (Git clone)
```
git clone -b [awx-tag-version] https://github.com/ansible/awx
git clone -b [awx-tag-version] https://github.com/ansible/awx [dir_name]
```
예시)
```
mkdir ansible-awx
cd ansible-awx
git clone -b 17.1.0 https://github.com/ansible/awx awx-17.0.1
```

### 2. Inventory Modify
* 내려 받은 source의 `installer` 경로로 이동 하여 `inventory`파일 수정
* `/installer/inventory` 파일에는 AWX 설치 및 옵션등에 대한 다양한 환경 설정이 가능함
  ```
  cd /ansible-awx/awx-17.0.1/installer
  vi inventory
  ```

* 예시) 기본 ADMIN 계정 설정 (필수)
    ```ini
    # This will create or update a default admin (superuser) account in AWX, if not provided
    # then these default values are used
    admin_user=admin
    # admin_password=password
    ```
    ```
    admin_password=admin1234    # 주석 해제 및 원하는 Default 계정의 PW 입력
    ```

* 예시) Docker 설정 (선택)
    ```ini 
    # Common Docker parameters
    awx_task_hostname=awx
    awx_web_hostname=awxweb
    # Local directory that is mounted in the awx_postgres docker container to place the db in
    postgres_data_dir="~/.awx/pgdocker"
    host_port=80
    host_port_ssl=443
    #ssl_certificate=
    # Optional key file
    #ssl_certificate_key=
    docker_compose_dir="~/.awx/awxcompose"
    ```
    ```
    host_port=8880 # AWX Web 접근 Port 변경 8880 (Docker Port forwarding) 
    ```

* 예시) Ansible Project 디렉토리 설정 (선택)
    ```
    # AWX project data folder. If you need access to the location where AWX stores the projects
    # it manages from the docker host, you can set this to turn it into a volume for the container.
    #project_data_dir=/var/lib/awx/projects
    ```
    ```
    project_data_dir=/root/ansible-awx/ansible-project  # 주석 해제로 활성화 및 경로 설정
    ```

### 3. Install (Play book Execute)
* `installer`경로로 들어가서 `install.yml` play-book 실행
  ```
  ansible-playbook -i inventory install.yml
  ```
  설치 (성공)
  * docker container 4개 활성화 확인
  ```
  docker ps -a
  
  adbd
  ```
  | Container Name | Description               |
    |----------------|---------------------------|
  | awx_task       | 실제 작업을 수행하는 역할을 하는 컨테이너   |
  | awx_web        | AWX의 Web Application 컨테이너 |
  | awx_redis      | 캐싱 및 큐 관리                 |
  | awx_postgres   | DB                        |

  설치 실패
  * `ansible-playbook -i inventory install.yml -vvv` 로 세부 오류 확인 후 작업
  * 아래와 같이 세부 로그 확인 가능
  ```
  fatal:: FAILED! => {
    ...
    ...
  }
  ```
### 4. 삭제
* awx 관련 도커 관련 데이터는 `/.awx` 숨김 폴더로 되어 있음 
  * `rm -rf .awx`명령으로 디렉토리 전체 삭제
  * docker container 및 image, volumes 등 제거



### 오류 사항
**local_docker : Check for existing Postgres data**
* `/installer/roles/local_dokcer/upgrade_postgres.yml` 파일 안에 해당 Task 내용을 보니 `ignore_errors: true` 옵션 확인 되어 무시
```
TASK [local_docker : Check for existing Postgres data (run from inside the container for access to file)] **************
fatal: [localhost]: FAILED! => {"changed": true, "cmd": "docker run --rm -v '/root/.awx/pgdocker:/var/lib/postgresql'
 centos:8 bash -c  \"[[ -f /var/lib/postgresql/10/data/PG_VERSION ]] && echo 'exists'\"\n", "delta": "0:00:00.924347", 
 "end": "2024-12-11 13:56:34.551841", "msg": "non-zero return code", "rc": 1, "start": "2024-12-11 13:56:33.627494", 
 "stderr": "", "stderr_lines": [], "stdout": "", "stdout_lines": []}
```















  

  


