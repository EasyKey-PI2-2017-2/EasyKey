FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN apt-get update
RUN apt-get install -y build-essential cmake pkg-config
RUN apt-get install -y libjpeg62-turbo-dev libtiff5-dev libjasper-dev libpng12-dev
RUN pip install -r requirements.txt
ADD . /code/
