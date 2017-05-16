FROM python:latest

EXPOSE 5000
#ADD . /code
#WORKDIR /code
RUN pip install flask
RUN pip install flask-mysql
RUN pip install pytest
RUN pip install fabric3
RUN pip install flask-talisman
