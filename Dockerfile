FROM python:3.6

RUN apt update && apt install -y openjdk-11-jdk git bc
RUN pip install gitpython
