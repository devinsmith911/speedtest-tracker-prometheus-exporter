FROM python:3.9.19-slim

ENV PORT=8080

WORKDIR app 
COPY ./requirements.txt requirements.txt

RUN pip3 install -r requirements.txt 

COPY . .

ENTRYPOINT gunicorn -w 1 -b 0.0.0.0:$PORT main:app