# midog

This project was generated via [manage-fastapi](https://ycd.github.io/manage-fastapi/)! :tada:

## License

This project is licensed under the terms of the None license.

## Before you run this server...
1. Set up the .env file
2. Create a venv, then install all requirements
3. Do the migration, then run init_db.py

## Run Server

uvicorn app.main:app --reload, or use start.sh

## Migration

alembic revision --autogenerate -m "描述"
alembic upgrade head

## Connect to Database

export PGPASSWORD="0113lisiyu"
psql -h localhost -U lisiyu0113 -d midogdaily
