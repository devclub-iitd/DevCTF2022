FROM tiangolo/uwsgi-nginx-flask:python3.10



WORKDIR /app
ENV STATIC_PATH /app/static


COPY ./requirements.txt ./requirements.txt
COPY ./pandoc-2.18-1-amd64.deb ./pandoc-2.18-1-amd64.deb

RUN apt update -y && apt install -y ./pandoc-2.18-1-amd64.deb
RUN pip install -r ./requirements.txt


COPY mandir /tmp/mandir
WORKDIR /tmp/mandir
RUN chmod +x ./create_man.sh
RUN ./create_man.sh
RUN rm -rf /tmp/mandir


RUN adduser \
    --disabled-login \
    -u 1001 \
    --gecos "" \
    --shell /bin/bash \
    ctf
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf 
WORKDIR /app