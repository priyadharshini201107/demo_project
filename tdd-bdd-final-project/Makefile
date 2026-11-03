install:
	pip install -r requirements.txt

test:
	nosetests -v

bdd:
	behave

lint:
	flake8 service tests features app.py

validate: lint test
