###
# Run
###

run:
	poetry run uvicorn main:app --port 8000 --reload

###
# Migrations
###

migrations:
	poetry run alembic revision --autogenerate

upgrade:
	poetry run alembic upgrade head


###
# Linter Tests
###

radon:
	poetry run radon mi -s -n B .

bandit:
	poetry run bandit -c configs/bandit.yaml -r app

mypy:
	poetry run mypy .

ruff_check:
	poetry run ruff check . --fix --preview

ruff_format:
	poetry run ruff format .

ltest: ruff_format ruff_check bandit radon mypy