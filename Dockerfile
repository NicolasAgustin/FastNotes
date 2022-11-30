FROM python:3.8

WORKDIR /application

COPY ./api /application/api

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY bootstrap.sh /etc/bootstrap.sh
RUN chmod a+x /etc/bootstrap.sh

# Flask
EXPOSE 5000

# Debugpy
EXPOSE 3003

CMD ["/etc/bootstrap.sh"]