init:
	pip install pipenv --upgrade
	pipenv install --dev

ci:
	pipenv run pytest

flake8:
	pipenv run flake8
