# FROM python:3.11-slim
# WORKDIR /app
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
# COPY . .
# CMD ["python", "-m", "src.tgbot.main"]


FROM python:3.12-slim
WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app/src/

ENV PYTHONUNBUFFERED=1 PYTHONFAULTHANDLER=1

WORKDIR /app/src
CMD ["python", "-m", "tgbot.main"]
