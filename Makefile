.PHONY: lint test

start:
	python main.py

nitpick:
	poetry run nitpick check

lint:
	poetry run flake8 .

test:
	poetry run pytest

test_cov:
	pytest --cov=.

test_report:
	pytest --cov=. --cov-report=xml