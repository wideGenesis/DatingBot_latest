# pull official base image
FROM python:3.9.12-bullseye
y
# set environment variables
ENV HOME=/home/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
#ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1


RUN mkdir -p $HOME

# set work directory
WORKDIR $HOME

# Run apt-get, to install the SSH server, and supervisor
RUN apt-get update
#    && apt-get install -y openssl libssl-dev cargo gcc musl-dev python3-dev libffi-dev openssl-dev

RUN pip install --upgrade pip
COPY requirements.txt /$HOME/requirements.txt
RUN pip install --no-cache-dir --no-deps -r requirements.txt

#
COPY . /$HOME

#
#CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
CMD [ "python", "./workers.py"]
#CMD [ "pypy3", "./workers.py"]


#https://hub.docker.com/_/pypy