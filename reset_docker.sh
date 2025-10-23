
#!/bin/bash

# 주의: 절대 서버에서 사용하지 않기
set +e

# 1️⃣ 모든 컨테이너 중지 및 삭제
docker stop $(docker ps -aq)
docker rm -f $(docker ps -aq)

# 2️⃣ 모든 이미지 삭제
docker rmi -f $(docker images -q)

# 3️⃣ 모든 볼륨 삭제
docker volume rm $(docker volume ls -q)

# 4️⃣ 모든 네트워크 삭제 (기본 네트워크 제외)
docker network rm $(docker network ls -q)

# 5️⃣ 빌드 캐시 완전 삭제
docker builder prune -a --force

# 6️⃣ 시스템 전체 정리 (불필요한 리소스 전부, DB 포함)
docker system prune -a --volumes --force
