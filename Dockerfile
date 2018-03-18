# FROM ubuntu:14.04
# MAINTAINER Edgar Felizmenio "edgarfelizmenio@gmail.com"
# RUN apt-get -y -q install python-pip
# RUN apt-get -y -q install libssl-dev libffi-dev python3-dev
# RUN apt-get -y -q install python3-pip
# RUN apt-get -y -q install python3.4-venv

# # put nginx on a separate container
# # put mysql on a separate container

# RUN pyvenv-3.4 
 
# # post install

# EXPOSE 22 80

# # copy startup script
# COPY 
# # run container
# CMD [""]

FROM python:3.4-alpine
MAINTAINER Edgar Felizmenio "edgarfelizmenio@gmail.com"

ADD . /code
WORKDIR /code
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn

# CMD ["gunicorn", "--worker-class gthread", "-w 1", "--threads 1", "app:app"]
