FROM python:3.7-slim

WORKDIR /web

ADD . /web

RUN apt-get update
RUN apt-get install -y build-essential python3-dev nano lsof
#cmake libzmq3-dev

RUN pip install -r requirements.txt
RUN usermod --non-unique --uid 1000 www-data \
  && groupmod --non-unique --gid 1000 www-data \
  && chown -R www-data:www-data /web

ENV FLASK_RUN_HOST=0.0.0.0
#USER www-data


ENV PYTHONDONTWRITEBYTECODE=1

#CMD ["flask", "run"]
CMD ["uwsgi", "--ini", "uwsgi.ini"]
