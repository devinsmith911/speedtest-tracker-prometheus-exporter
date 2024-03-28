from prometheus_client import Summary, Gauge, generate_latest, CONTENT_TYPE_LATEST
from flask import Flask, Response
import time
import requests 
import os
import logging 

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(format='%(asctime)s %(levelname)s - %(message)s', level=LOG_LEVEL)

logging.info("Starting Speedtest Tracker Prometheus Exporter")
app = Flask('app')

API_URL = os.environ['SPEEDTEST_API_URL']
URL_SUBPATH = os.environ.get('URL_SUBPATH', '/api/speedtest/latest' )
FULL_API_URL = ('{}{}').format(API_URL, URL_SUBPATH)
METRICS_ENDPOINT = os.environ.get('METRICS_ENDPOINT', '/metrics')

LAST_SPEEDTEST_UP = Gauge('upload_speed', 'Last value of upload speed for test')
LAST_SPEEDTEST_DOWN = Gauge('download_speed', 'Last value of download speed for test')
LAST_SPEEDTEST_PING = Gauge('ping', 'Last value of ping latency for test')
COLLECTION_TIME = Gauge('collection_time', 'Time of the last collection')

def get_metrics_data(FULL_API_URL):
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
    logging.debug("Starting collection from {}".format(FULL_API_URL))
    speedtest_data = get_metrics_data(FULL_API_URL)
    upload, download, ping = collect_data(speedtest_data)
    logging.debug("Collection complete, Setting metrics")
    LAST_SPEEDTEST_DOWN.set(download)
    LAST_SPEEDTEST_UP.set(upload)
    LAST_SPEEDTEST_PING.set(ping)
    COLLECTION_TIME.set(collection_time())
    logging.debug("Metrics Set")
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)