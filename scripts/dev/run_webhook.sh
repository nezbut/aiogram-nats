#!/bin/bash

export AIOGRAM_NATS_BOT__TOKEN__VALUE=bottoken

export AIOGRAM_NATS_BOT__BOT_API__TYPE=local
export AIOGRAM_NATS_BOT__BOT_API__API_URL=http://localhost:8081
export AIOGRAM_NATS_BOT__BOT_API__FILE_URL=http://localhost:80

export AIOGRAM_NATS_BOT__WEBHOOK__URL=http://nginx
export AIOGRAM_NATS_BOT__WEBHOOK__SECRET_TOKEN__VALUE=dfajidjfoijfiffwsf
export AIOGRAM_NATS_BOT__WEBHOOK__WEBHOOK_PATH=webhook

export AIOGRAM_NATS_BOT__FSM_STORAGE__NATS__CREATE_NATS_KV_BUCKETS=true

export AIOGRAM_NATS_DB__RDB__USERNAME=superuser
export AIOGRAM_NATS_DB__RDB__PASSWORD__VALUE=password
export AIOGRAM_NATS_DB__RDB__PORT=5430


# export AIOGRAM_NATS_BROKER__NATS__SERVERS="[{host='nats'}]"
export AIOGRAM_NATS_LOGGING__DEV=true

# gunicorn -w 4 --worker-class aiohttp.GunicornWebWorker --bind localhost:8080 aiogram_nats.__main__:main
python -m aiogram_nats