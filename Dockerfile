FROM python:3.9.19-slim

WORKDIR app 
COPY ./requirements.txt requirements.txt

RUN pip3 install -r requirements.txt 

COPY . .

ENTRYPOINT ["gunicorn", "-w 4", "-b 0.0.0.0:8080", "main:app"]