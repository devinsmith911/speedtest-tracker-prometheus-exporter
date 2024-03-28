from prometheus_client import Summary, Gauge, generate_latest, CONTENT_TYPE_LATEST
import time
import requests 
import os
from flask import Flask, Response

app = Flask('app')

API_URL = os.environ.get('SPEEDTEST_API_URL', 'http://localhost')
URL_SUBPATH = os.environ.get('URL_SUBPATH', '/api/speedtest/latest' )
FULL_API_URL = ('{}{}').format(API_URL, URL_SUBPATH)
METRICS_ENDPOINT = os.environ.get('METRICS_ENDPOINT', '/metrics')

LAST_SPEEDTEST_UP = Gauge('upload_speed', 'Last value of upload speed for test')
LAST_SPEEDTEST_DOWN = Gauge('download_speed', 'Last value of download speed for test')
LAST_SPEEDTEST_PING = Gauge('ping', 'Last value of ping latency for test')
COLLECTION_TIME = Gauge('collection_time', 'Time of the last collection')

def get_metrics_data():
    speedtest_data = requests.get(FULL_API_URL).json()
    return speedtest_data

def collect_data(speedtest_data):
    upload = speedtest_data['data']['upload']
    download = speedtest_data['data']['download']
    ping = speedtest_data['data']['ping']
    return upload, download, ping

def collection_time():  
    current_time = time.time()
    return current_time

@app.route(METRICS_ENDPOINT)
def get_metrics():
    speedtest_data = get_metrics_data()
    upload, download, ping = collect_data(speedtest_data)
    LAST_SPEEDTEST_DOWN.set(download)
    LAST_SPEEDTEST_UP.set(upload)
    LAST_SPEEDTEST_PING.set(ping)
    COLLECTION_TIME.set(collection_time())
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)