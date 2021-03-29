FROM ubuntu:20.04

# docker build -t rust-detector:v1.0 .

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

RUN apt-get update && \
    apt-get install -y apt-utils && \
    apt-get install -y python3

COPY . /opt/task/

ENTRYPOINT ["python3", "/opt/task/detect_rust.py"]
