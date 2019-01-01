# Prometheus Exporter for Nest API

This is application fetches metrics from the Nest Thermostat api using the [python-nest](https://github.com/jkoelker/python-nest) library and exposes them using the [prometheus_client](https://github.com/prometheus/client_python) library.

See `example/` folder for example outputs.

## Dev environment
`docker run --rm -ti -v $(pwd):/app -w /app --entrypoint sh -p 8080:8000 python:3-alpine`

- pip install -r requirements.txt

- python metrics.py
