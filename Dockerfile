FROM python:latest

EXPOSE 5000
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD python app.py