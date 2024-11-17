#!/bin/bash

export AIOGRAM_NATS_BOT__TOKEN__VALUE=bottoken
export AIOGRAM_NATS_DB__RDB__USERNAME=superuser
export AIOGRAM_NATS_DB__RDB__PASSWORD__VALUE=password
export AIOGRAM_NATS_DB__RDB__PORT=5430

taskiq scheduler aiogram_nats.infrastructure.scheduler.taskiq_constants:taskiq_scheduler -tp **/tasks.py -fsd