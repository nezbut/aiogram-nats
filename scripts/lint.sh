#!/bin/bash

export MYPYPATH=D:\\MyProjectPython\\aiogram-nats\\aiogram_nats\\stubs

poetry run ruff check .
poetry run mypy . --exclude aiogram_nats/stubs
