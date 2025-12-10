FROM python:3.13-slim

WORKDIR /app
EXPOSE 8000

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

ADD . .

CMD [ "python3", "main.py" ]
