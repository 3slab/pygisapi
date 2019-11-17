.PHONY: init ci flake8 run
.DEFAULT_GOAL := run

init:
	pip install pipenv --upgrade
	pipenv install --dev

ci:
	pipenv run pytest

flake8:
	pipenv run flake8

run:
	pipenv run uvicorn app.main:app --reload