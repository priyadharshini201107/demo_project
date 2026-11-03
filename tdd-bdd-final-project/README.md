# Product Management Microservice

A small Flask REST API for managing products. This repository contains the application, unit tests, Behave feature files, a GitHub Actions workflow, and Tekton task definitions.

## Requirements
- Python 3.10+
- pip

## Run locally
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
The API listens on `http://127.0.0.1:8000`.

## Run tests
```bash
nosetests
behave
flake8 service tests features app.py
```

## API endpoints
- `GET /products` — list products
- `POST /products` — create a product
- `GET /products/<id>` — retrieve a product
- `PUT /products/<id>` — update a product
- `DELETE /products/<id>` — delete a product

## GitHub Actions
The workflow in `.github/workflows/workflow.yml installs dependencies, runs flake8, and runs nose tests on pushes and pull requests.

## Tekton
`.tekton/tasks.yml` contains cleanup and test tasks. These are task definitions; a working pipeline also requires a Pipeline resource and a configured Tekton installation/namespace.
