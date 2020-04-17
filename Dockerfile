FROM python:3

RUN mkdir /app

WORKDIR /app

COPY ./requirements.txt /app/

RUN pip install -r requirements.txt

COPY ./set_env.sh /app/

ADD . /app

CMD [ "python", "slavkabot/main.py" ]