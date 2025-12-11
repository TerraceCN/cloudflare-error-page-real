FROM python:3.13-slim

LABEL org.opencontainers.image.source=https://github.com/donlon/cloudflare-error-page
LABEL org.opencontainers.image.description="Create a Cloudflare error page with real-time edge location data."
LABEL org.opencontainers.image.licenses=MIT

WORKDIR /app
EXPOSE 8000

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

ADD . .

CMD [ "python3", "main.py" ]
