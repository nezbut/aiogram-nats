FROM python:3.11-slim-bullseye as builder
ENV VIRTUAL_ENV=/opt/venv
ENV CODE_PATH=/source
RUN pip3 install --no-cache-dir poetry==1.8.2
RUN python3 -m venv $VIRTUAL_ENV
WORKDIR $CODE_PATH
COPY poetry.lock pyproject.toml ${CODE_PATH}/
RUN python3 -m poetry export -f requirements.txt | $VIRTUAL_ENV/bin/pip install -r /dev/stdin

FROM python:3.11-slim-bullseye as run-image
ENV VIRTUAL_ENV=/opt/venv
ENV CODE_PATH=/source
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV
COPY . ${CODE_PATH}/aiogram_nats
WORKDIR $CODE_PATH/aiogram_nats
ENTRYPOINT ["python3", "-m", "aiogram_nats"]