# From: https://opensource.com/article/19/4/weather-python-prometheus

import requests

# add your proxies if necessary
http_proxy  = ''
https_proxy = ''

proxyDict = {
              "http"  : http_proxy,
              "https" : https_proxy
            }

HOURLY_SAN_BRUNO = 'https://api.weather.gov/gridpoints/MTR/86,120/forecast/hourly'

# get hourly temperature
def get_temperature():
    result = requests.get(HOURLY_SAN_BRUNO, proxies=proxyDict)
    return result.json()["properties"]["periods"][0]["temperature"]

# test usa gov weather api
# print(get_temperature())

# create a registry with temperature gauge
from prometheus_client import CollectorRegistry, Gauge
def prometheus_temperature(num):
    registry = CollectorRegistry()
    g = Gauge("san_bruno_temp", "Temperature at San Bruno", registry=registry)
    g.set(num)
    return registry


# build a simple web server with pyramid
from pyramid.config import Configurator
from pyramid.response import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

def metrics_web(request):
    registry = prometheus_temperature(get_temperature())
    return Response(generate_latest(registry),
                   content_type=CONTENT_TYPE_LATEST)

config = Configurator()
config.add_route('metrics', '/metrics')
config.add_view(metrics_web, route_name='metrics')
app = config.make_wsgi_app()

# run with any Web Server Gateway Interface (WSGI) server
# python -m twisted web --wsgi weather.app
