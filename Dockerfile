FROM python:3.8

COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN pip install -r requirements.txt --no-cache-dir

COPY . /

CMD [ "python", "main.py", "-c", "config.yml"]
