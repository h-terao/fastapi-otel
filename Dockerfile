FROM python:3.12-slim AS builder

# Install uv
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /workspace

COPY ./pyproject.toml .
COPY ./uv.lock .
COPY ./main.py ./main.py

RUN uv sync --frozen

ENV TZ Asia/Tokyo
EXPOSE 8002

CMD ["uv", "run", "python", "main.py"]