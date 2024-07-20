FROM alpine
RUN apk update
RUN apk upgrade
RUN apk add git
RUN apk add docker
RUN apk add docker-compose
RUN apk add openrc --no-cache
RUN git clone --depth 1 https://github.com/dzamakhaiev/messenger.git
RUN rc-update add docker boot
WORKDIR /messenger
