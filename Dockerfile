FROM python:3-alpine

LABEL org.opencontainers.image.authors="daniel@megye.si" \
      org.opencontainers.image.source="https://github.com/dmegyesi/nest-prometheus"

# At the time of building the image, with your CI pipeline add the image creation date (force UTC with -u) and the git hash:
# docker build
# --label org.opencontainers.image.revision=$CI_COMMIT_SHA
# --label org.opencontainers.image.created=$(date -u "+%Y-%m-%dT%T+00:00")
# .

EXPOSE 8000

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["/app/metrics.py"]
