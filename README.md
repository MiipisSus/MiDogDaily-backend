# midog

This project was generated via [manage-fastapi](https://ycd.github.io/manage-fastapi/)! :tada:

## License

This project is licensed under the terms of the None license.

## Run Server

uvicorn app.main:app --reload

## Migration

alembic revision --autogenerate -m "描述"
alembic upgrade head

## Connect to Database

export PGPASSWORD="0113lisiyu"
psql -h localhost -U lisiyu0113 -d midogdaily
