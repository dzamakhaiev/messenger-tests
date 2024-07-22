FROM python:3-alpine
ENV RUN_INSIDE_DOCKER 1
RUN apk update
RUN apk upgrade
RUN apk add git
RUN git clone --depth 1 https://github.com/dzamakhaiev/messenger-tests.git
WORKDIR /messenger-tests
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt --break-system-packages
#CMD python3 -m unittest discover integration > test_results.txt