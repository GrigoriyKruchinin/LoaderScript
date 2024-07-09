.PHONY: lint test

start:
	python main.py

lint:
	flake8 .

test:
	pytest .