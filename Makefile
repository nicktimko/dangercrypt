SHELL := bash
.ONESHELL:
.SHELLFLAGS := -o errexit -o nounset -o pipefail -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

python_version := 3.10
venv_dir := .venv
venv_python := ${venv_dir}/bin/python${python_version}

# VARIABLES
container := dangercrypt-testing
docker_run_args := \
	--env VENV_FOLDER_NAME=".test_venv_container" \
	--rm \
	--volume $(shell pwd):/app

docker_run_as_user := --user $(shell id -u):$(shell id -g)

# TARGETS

.PHONY: all clean test_local test containertest

all: build test

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

test:
	${venv_python} -m pytest --cov-report=html --cov=dangercrypt tests

containertest:
	docker run $(docker_run_args) $(docker_run_as_user) $(container) make test

venv: requirements/testing.txt
	rm -rf ${venv_dir}
	python${python_version} -m venv ${venv_dir}
	# skipping hashes for lib testing
	${venv_dir}/bin/python -m pip install \
		--disable-pip-version-check \
		--requirement $<
	${venv_dir}/bin/python -m pip list > $@

requirements/testing.txt: requirements/testing.in
	pip-compile --quiet --generate-hashes --output-file=$@ $<
