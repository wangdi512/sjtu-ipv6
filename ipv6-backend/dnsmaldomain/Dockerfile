FROM python:2.7

RUN mkdir /code
ADD ./code/requirements.txt /code
RUN pip install -r /code/requirements.txt
ADD ./code/ /code
WORKDIR /code 

ENTRYPOINT ["/code/entrypoint.sh"]
