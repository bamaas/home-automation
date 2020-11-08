FROM jfloff/alpine-python:3.8-slim

WORKDIR /srv

COPY ./requirements.txt /srv

COPY ./backup.py ./srv

# install Docker
RUN echo "http://dl-cdn.alpinelinux.org/alpine/latest-stable/community/" >> /etc/apk/repositories
RUN apk add libxml2-dev libxslt-dev python-dev
RUN apk add --update --no-cache --virtual .build-deps \
        g++ \
        python-dev \
        libxml2 \
        libxml2-dev && \
        apk add libxslt-dev
RUN apk add py3-lxml
RUN pip install --no-cache-dir -r requirements.txt
RUN apk del .build-deps

CMD ["python", "backup.py"]