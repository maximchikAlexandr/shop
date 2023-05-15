FROM python:3.11

SHELL ["/bin/bash", "-c"]

# set the environment variables
ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.3.2


RUN pip install --upgrade pip
RUN pip install "poetry==$POETRY_VERSION"
RUN useradd -rms /bin/bash shop && chmod 777 /opt /run

# mkdir + cd
WORKDIR /app

RUN chown -R shop:shop /app && chmod 755 /app

COPY --chown=shop . .
RUN poetry config virtualenvs.create false && poetry config installer.max-workers 10 \
&& poetry install --no-root