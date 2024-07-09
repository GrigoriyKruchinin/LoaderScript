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
	pytest --cov=./repo_downloader

test_report:
	pytest --cov=./repo_downloader --cov-report=xml