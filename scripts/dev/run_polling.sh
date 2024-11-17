#!/bin/bash

# export AIOGRAM_NATS_BOT__BOT_API__TYPE=local
# export AIOGRAM_NATS_BOT__BOT_API__API_URL=http://localhost:8081
# export AIOGRAM_NATS_BOT__BOT_API__FILE_URL=http://localhost:80

export AIOGRAM_NATS_BOT__TOKEN__VALUE=bottoken

export AIOGRAM_NATS_BOT__FSM_STORAGE__NATS__CREATE_NATS_KV_BUCKETS=true

export AIOGRAM_NATS_DB__RDB__USERNAME=superuser
export AIOGRAM_NATS_DB__RDB__PASSWORD__VALUE=password
export AIOGRAM_NATS_DB__RDB__PORT=5430
export AIOGRAM_NATS_LOGGING__DEV=true

python -m aiogram_nats