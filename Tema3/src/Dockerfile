FROM python:latest

COPY requirements.txt /tmp
RUN pip3 install --upgrade pip && \
    pip3 install -r /tmp/requirements.txt && \
    apt-get update && apt-get install -y netcat-traditional

ADD server.py start_server.sh /server/
WORKDIR /server

ADD start_server.sh /
RUN chmod +x /start_server.sh

CMD ["./start_server.sh"]
