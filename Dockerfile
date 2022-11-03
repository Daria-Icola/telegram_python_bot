FROM python:3.9
MAINTAINER "Daria-Icola"

ENV PYTHONPATH=/app

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD python src/main.py
