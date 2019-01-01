FROM python:3.6-alpine
WORKDIR /bot
COPY . /bot
RUN pip install --trusted-host pypi.python.org -r requirements.txt
CMD [ "python", "bot.py" ]
