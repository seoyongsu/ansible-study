# AWX Operator
AWX 18 버전 부터는 Operator를 이용한 설치 방식으로 전환


#### Git
https://github.com/ansible/awx-operator
#### 공식 문서
https://ansible.readthedocs.io/projects/awx-operator/en/latest/



# 필수 패키지
* Kubernetes
* make


# Install
### 1. ansible-operator 소스 clone
``` shell
git clone -b <<tag-version>> https://github.com/ansible/awx-operator
```

### 2. make 파일 실행
```
$ cd awx-operator
$ make deploy
```
* `awx`로 namespace가 생성됩니다.
* awx `awx-operator-controller-manager...`이라는 pods가 생성됩니다.
```shell
kubectl get pods -n awx
```


### 3. AWX 설치
CR 파일을 작성 하여 설치

#### Base install
``` shell
# kubectl create -f << file >> -n << namepase >>
kubectl create -f awx-demo.yml -n awx
```
``` yaml
# awx-demo.yml
---
apiVersion: awx.ansible.com/v1beta1
kind: AWX
metadata:
  name: awx-demo
spec:
  service_type: nodeport
```

#### External DB 설정 방법
awx db 정보에 대한 secret 생성
``` yaml
# awx-postgres-configuration.yml
---
apiVersion: v1
kind: Secret
metadata:
  name: awx-postgres-configuration
stringData:
  host: << database host >>
  port: << database port >>
  database: << database name >>
  username: << database user >>
  password: << database password >>
  target_session_attrs: "read-write"
  type: "unmanaged"
type: Opaque
```
```shell
kubectl create -f awx-postgres-configuration.yml -n awx
```

AWX 실행 CR에 secret 선언
```yaml
---
apiVersion: awx.ansible.com/v1beta1
kind: AWX
metadata:
  name: awx-demo
spec:
  service_type: nodeport
  
  # K8S secret Database Config
  postgres_configuration_secret: awx-postgres-configuration
```

## 4. ADMIN PW 확인
네임스페이스의 secret 목록에서 ...admin-password라는 secret 확인
```shell
kubectl get secret -n awx
```
```
NAME                           TYPE                DATA   AGE
awx-demo-admin-password             Opaque              1      26m
awx-demo-app-credentials            Opaque              3      26m
awx-demo-broadcast-websocket        Opaque              1      26m
awx-postgres-configuration     Opaque              7      26m
awx-demo-receptor-ca                kubernetes.io/tls   2      26m
awx-demo-receptor-work-signing      Opaque              2      26m
awx-demo-secret-key                 Opaque              1      26m
redhat-operators-pull-secret   Opaque              1      26m
```
```shell
# kubectl get secret << secret name >> -n << name space >> -o jsonpath="{.data.password}" | base64 --decode ; echo 
kubectl get secret awx-demo-admin-password -n awx -o jsonpath="{.data.password}" | base64 --decode ; echo
```


## 접속 확인
``` shell
# 서비스의 포토 확인
kubectl get svc -n awx
```
```
NAME                                              TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
awx-operator-controller-manager-metrics-service   ClusterIP   10.43.63.169   <none>        8443/TCP       24m
awx-service                                       NodePort    10.43.17.242   <none>        80:30080/TCP   23m
```













