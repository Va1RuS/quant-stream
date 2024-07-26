#!/bin/bash

# Stop on error
set -e

# Run Alembic Upgrade
alembic upgrade head

# Start Uvicorn
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
