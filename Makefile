PROJECT := invest_api
VERSION := $(shell git describe --tags `git rev-list --tags --max-count=1`)

VENV := .venv
export PATH := $(VENV)/bin:$(PATH)

REPORTS := .reports
COVERAGE := $(REPORTS)/coverage

SOURCES := $(PROJECT) gunicorn.config.py
TESTS := tests
MIGRATIONS := migrations

IMAGE_NAME := $(PROJECT)
AZURE_IMAGE_TAG := altdata.azurecr.io/invest/$(IMAGE_NAME):$(VERSION)

clean:
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf $(REPORTS)
	rm -rf $(VENV)

.venv:
	poetry install --no-root
	poetry check

.reports:
	mkdir $(REPORTS)

setup: .venv .reports

install: setup

update: setup
	poetry update

isort: setup
	isort -rc $(SOURCES) $(TESTS) $(MIGRATIONS)

mypy: setup
	mypy $(SOURCES) $(TESTS) $(MIGRATIONS)

pylint: setup
	pylint $(SOURCES) $(TESTS) $(MIGRATIONS) > $(REPORTS)/pylint.txt

flake: setup
	flake8 $(SOURCES) $(TESTS) $(MIGRATIONS)

bandit: setup
	bandit -f json -o $(REPORTS)/bandit.json -r $(SOURCES) $(TESTS) $(MIGRATIONS) -s B101

test: setup
	pytest

cov: setup
	coverage run --source $(PROJECT) --module pytest
	coverage report
	coverage html -d $(COVERAGE)/html
	coverage xml -o $(COVERAGE)/cobertura.xml
	coverage erase
	cobertura-clover-transform $(COVERAGE)/cobertura.xml -o $(COVERAGE)/clover.xml

lint: isort mypy pylint flake bandit test

build: lint cov
	docker build . -t $(IMAGE_NAME) --pull

deploy: build
	docker tag $(IMAGE_NAME):latest $(AZURE_IMAGE_TAG)
	docker push $(AZURE_IMAGE_TAG)

all: lint cov build

.DEFAULT_GOAL := all
