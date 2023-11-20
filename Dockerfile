FROM python:3.10-bullseye

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Moscow
ENV SECRET_KEY="StrongSecretKey"
RUN apt-get update && apt-get install -y software-properties-common python3-pip git curl sudo postgresql postgresql-contrib tzdata -y

RUN service postgresql start &&\
  sudo -i -u postgres psql -c "create database ecommerce;" &&\
  sudo -i -u postgres psql -c "create user administer with encrypted password 'securepassword'; grant all privileges on database ecommerce to administer;" && service postgresql stop

COPY . /Ecommerce-API
WORKDIR /Ecommerce-API

RUN pip install -r requirements.txt
RUN pip install httpx
RUN pip install python-jose
RUN chmod +x /Ecommerce-API/script.sh

EXPOSE 8000

ENTRYPOINT [ "bash", "/Ecommerce-API/script.sh" ] 