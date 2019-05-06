# prometheus-weather-exporter

Prometheus exporter to get next hour temperature of a city, e.g. (San Bruno, CA).

Ref here how to get the gridpoints API endpoint for your city:

https://www.weather.gov/documentation/services-web-api

## Install

`pip install -r requirements.txt`

## Usage


```bash
$ python -m twisted web --wsgi weather.app
```

## Test

```bash
$ curl http://localhost:8080/metrics
# HELP san_bruno_temp Temperature at San Bruno
# TYPE san_bruno_temp gauge
san_bruno_temp 56.0
```
