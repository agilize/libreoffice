FROM python:3-alpine

LABEL maintainer='dev@agilize.com.br'

# packages
RUN apk add --no-cache \
    dumb-init \
    openjdk8 \
    libreoffice \
    libreoffice-base \
    libreoffice-lang-de \
    mesa-gl \
    ttf-freefont

RUN apk add --no-cache \
	bash

# python installs
RUN pip install \
	werkzeug \
	executor \
	gunicorn

# copy app
COPY app.py .

# port expose
EXPOSE 80

# entry point
ENTRYPOINT ["/usr/local/bin/gunicorn"]

# run app
CMD ["-b", "0.0.0.0:80", "--log-file", "-", "app:application"]