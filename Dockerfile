FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev

RUN pip install uv
COPY requirements.txt .
RUN uv pip install --no-cache-dir --system -r requirements.txt

COPY . .

CMD ["fastapi", "run", "app/main.py", "--port", "80", "--workers", "4"]