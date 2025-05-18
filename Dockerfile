FROM python:3.12.3-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONNUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install chromium
RUN apt-get update && apt-get install -y libglib2.0-0\
    libnss3\
    libnspr4\
    libdbus-1-3\
    libatk1.0-0\
    libatk-bridge2.0-0\
    libatspi2.0-0\
    libx11-6\
    libxcomposite1\
    libxdamage1\
    libxext6\
    libxfixes3\
    libxrandr2\
    libgbm1\
    libxcb1\
    libxkbcommon0\
    libasound2

COPY . .

CMD ["sh", "-c", "alembic upgrade head && python3 -m src.main"]