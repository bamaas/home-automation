FROM ubuntu:latest

WORKDIR /src

ARG USERNAME
ARG PASSWORD

RUN apt-get update && \
    apt-get install -y curl && \
    curl -fsSL https://filebrowser.xyz/get.sh | bash && \
    apt-get clean

COPY ./config/.filebrowser.json ./.filebrowser.json

RUN filebrowser config init && \
    filebrowser users add $USERNAME $PASSWORD

CMD filebrowser -c "./.filebrowser.json"
