# Prometheus client for Nest API

This is a client application which fetches
- the current state of my Nest thermostat
- the current weather conditions, based on the OpenWeatherMap API

See `example/` folder for example outputs.

## Dev environment
`docker run --rm -ti -v $(pwd):/app -w /app --entrypoint sh -p 8080:8000 python:3-alpine`

- pip install -r requirements.txt

- python metrics.py
