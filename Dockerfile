FROM python:3.14-slim

WORKDIR /app

COPY main.py sum.py sub.py ./

ENTRYPOINT ["python", "main.py"]
