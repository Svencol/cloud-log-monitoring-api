FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY test_api.py .
COPY example_logs.json .
COPY start.sh .

RUN chmod +x start.sh

CMD ["./start.sh"]