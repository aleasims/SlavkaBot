FROM python:3

RUN mkdir /app

WORKDIR /app

COPY ./requirements.txt /app/

RUN pip install -r requirements.txt --no-cache-dir

COPY ./env_vars.txt /app/

ADD . /app

CMD [ "python", "main.py" ]
