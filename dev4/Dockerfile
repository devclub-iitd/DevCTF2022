FROM tiangolo/uwsgi-nginx-flask:python3.10

WORKDIR /app

COPY ./requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

COPY ./app /app
# RUN adduser \
#     --disabled-login \
#     -u 1001 \
#     --gecos "" \
#     --shell /bin/bash \
#     ctf
# RUN chown 1001:1001 captcha.db
# RUN chmod 777 captcha.db
# COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf 