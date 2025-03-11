# k3s
K3s는 쿠버네티스와 완전히 호환되며 다음과 같은 향상된 기능을 갖춘 배포판


# Install
k3s 설치 방법
### 단일 노드 설치
``` shell
curl -sfL https://get.k3s.io | sh -
```
``` shell
# 설치 확인 및 실행 확인
sudo systemctl status k3s
```


### 멀티 노드 설치
마스터 노드
``` shell
curl -sfL https://get.k3s.io | sh -s - server --disable traefik
```
```shell
# 토큰 확인
sudo cat /var/lib/rancher/k3s/server/node-token
```
워커 노드
``` shell
curl -sfL https://get.k3s.io | K3S_URL="https://<MASTER_IP>:6443" K3S_TOKEN="<NODE_TOKEN>" sh -
```
