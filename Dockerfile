FROM python:3.10-slim-buster

EXPOSE 9999

WORKDIR /app

CMD ["./scripts/run-prod.sh"]
VOLUME ["/app/docs/"]

RUN adduser --uid 1000 --disabled-password --gecos '' --home /home/deploy deploy

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    python3-pip \
    netcat \
    postgresql-client && \
    rm -rf /var/lib/apt/lists/*

# Install 3rd party in deeper layer cause it changes less often
COPY requirements/ /app/requirements/
RUN pip install --no-cache-dir -r /app/requirements/dev.txt

COPY . /app
ENV PYTHONPATH=/app
RUN chown deploy.deploy -R /app

COPY docs/ /app/docs/
# RUN make -C /app/docs/ html

# Run everything as user deploy inside the container
USER deploy



#FROM tiangolo/uvicorn-gunicorn:python3.11-slim
#
#LABEL maintainer="Stelios Barberakis <chamalis@pm.me>"
#
#WORKDIR /app
#
## Install 3rd party in deeper layer cause it changes less often
#COPY requirements/ /app/requirements
#RUN pip install --no-cache-dir -r /app/requirements/docker.txt
#
## tiangolo's image expects /app/main.py or /app/app/main.py
#COPY ./app /app
#
## #COPY ./scripts /app/scripts
#CMD ["/app/scripts/run-prod.sh"]
## CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]



# ## MANUAL DOCKERFILE using custom run script run-prod.sh ## #

#FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11