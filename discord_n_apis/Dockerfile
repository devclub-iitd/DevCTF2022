FROM python:3
FROM gorialis/discord.py

RUN mkdir -p /usr/src/bot
COPY requirements.txt /usr/src/bot/requirements.txt
WORKDIR /usr/src/bot
RUN pip install -r requirements.txt

CMD [ "python", "-u", "main.py" ]