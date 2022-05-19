FROM tiangolo/uwsgi-nginx-flask:python3.10

COPY flag_dir/flag.txt /srv/http/app2/src/required_file
ENV FLAG_DIR /srv/http/app2/src/

WORKDIR /app
ENV STATIC_PATH /app/static

COPY ./requirements.txt ./requirements.txt

RUN apt update -y
RUN pip install -r ./requirements.txt

RUN adduser \
    --disabled-login \
    -u 1001 \
    --gecos "" \
    --shell /bin/bash \
    ctf
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf 

