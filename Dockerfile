# 빌드 스테이지 - Python 3.13 with Debian Bullseye
FROM python:3.13-slim AS builder

# 빌드 스테이지용 포트 환경 변수 설정
# docker-compose.yml의 .env 파일에서 BACKEND_PORT를 주입받음
ARG APP_PORT
ENV APP_PORT=${APP_PORT}

# 시스템 의존성 설치 및 보안 업데이트 적용
RUN apt-get update && apt-get install -y \
    gcc \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사
COPY Pipfile Pipfile.lock ./

# Python 의존성 설치
RUN pip install --no-cache-dir --upgrade pip pipenv && \
    pipenv install --system --deploy


# 최종 실행 스테이지
FROM python:3.13-slim

# 포트 환경 변수 설정
# docker-compose.yml의 .env 파일에서 BACKEND_PORT를 주입받음
ARG APP_PORT
ENV APP_PORT=${APP_PORT}

# Python 환경 변수 설정
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

# 런타임 의존성 설치 및 보안 업데이트 적용
RUN apt-get update && apt-get install -y \
    curl \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

# 비root 사용자 생성
RUN useradd -m -u 1000 appuser

# 작업 디렉토리 설정
WORKDIR /app

# 빌더 스테이지에서 설치된 패키지 복사
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# 애플리케이션 코드 복사
COPY --chown=appuser:appuser ./app ./app

# 비root 사용자로 전환
USER appuser

# 포트 노출
EXPOSE ${APP_PORT}

# 헬스체크 설정 (/health 엔드포인트 사용)
HEALTHCHECK --interval=30s --timeout=5s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:${APP_PORT}/health || exit 1

# Gunicorn + Uvicorn 워커로 애플리케이션 실행
CMD gunicorn app.main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:${APP_PORT} \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
