# pull official base image
FROM python:3.9.12-slim-bullseye

# create the app user
RUN addgroup --system app && adduser --system --group app

# set environment variables
  # python:
ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  POETRY_VERSION=1.1.13 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry'
  # appropriate directories:
ENV HOME=/home/app
ENV APP_ROOT=$HOME/mlnw
ENV PORT 8000

#Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpq-dev \
        build-essential \
        htop  \
        mc \
        nano \
    # Cleaning cache:
    && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/* \
    && pip install "poetry==$POETRY_VERSION" && poetry --version

# create directory for the app user
RUN mkdir -p $HOME \
    && mkdir -p $APP_ROOT \
    && mkdir -p $APP_ROOT/staticfiles \
    && mkdir -p $APP_ROOT/mediafiles \
    && mkdir -p $HOME/.cache/mc \
    && mkdir -p $APP_ROOT/logs/ \
    && touch $APP_ROOT/logs/debug_logs.log

# set work directory
WORKDIR $APP_ROOT

# copy whole project to docker home directory.
COPY . $APP_ROOT
COPY ./static/favicon/favicon.ico $APP_ROOT/staticfiles/favicon/
COPY ./static/robots.txt $APP_ROOT/staticfiles/robots.txt
RUN rm -rf $APP_ROOT/static_assets

# Install dependencies:
RUN poetry install

# copy entrypoint.prod.sh
#RUN sed -i 's/\r$//g'  $APP_ROOT/entrypoints/entrypoint_postgresql.sh
#RUN chmod +x  $APP_ROOT/entrypoints/entrypoint_postgresql.sh

# chown all the files to the app user
RUN chown -R app:app $HOME

# change to the app user
USER app

EXPOSE 8000
# run entrypoint.prod.sh
#ENTRYPOINT ["/home/app/mlnw/entrypoints/entrypoint_postgresql.sh"]
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

