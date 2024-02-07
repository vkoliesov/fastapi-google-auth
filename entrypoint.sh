#!/usr/bin/env sh

echo "Prepare migrations"
alembic upgrade head
echo "Done migrations"

echo "Run the server"
uvicorn main:app --host 0.0.0.0 --log-level info --reload --workers 4