#!/bin/bash
echo Starting server
poetry run alembic upgrade head
poetry run uvicorn app.main:app --workers 1 --host 0.0.0.0 --port 80 --forwarded-allow-ips='*' --proxy-headers
