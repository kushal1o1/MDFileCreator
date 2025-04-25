FROM python:3.9-slim-buster

RUN apt-get update && apt-get install -y \
    python3-tk \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

ENV DISPLAY=:99

WORKDIR /mdcreator

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["xvfb-run","-a", "python", "main.py"]

