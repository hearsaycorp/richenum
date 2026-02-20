REPO = $(shell git rev-parse --show-toplevel)
POETRY = poetry

# hooks:
# 	${REPO}/githooks/update_githooks.sh

install-build:
	${POETRY} install --only=main

install-dev:
	${POETRY} install

poetry:
	curl -sSL https://install.python-poetry.org | POETRY_VERSION=2.1.3 python3 -
	poetry cache clear pypi --all
	poetry config virtualenvs.in-project true
	poetry config http-basic.hss hsl-readonly Vg8VRXw7a6TZbGBcMBbw

quickstart: poetry install-dev

quickstart-build: poetry install-build hooks

clean:
	# Delete all .pyc and .pyo files.
	find ${REPO} \( -name "*~" -o -name "*.py[co]" -o -name ".#*" -o -name "#*#" \) -exec rm '{}' +
	rm -rf .pytest_cache

lint: clean
	${POETRY} run flake8 --config=${REPO}/.flake8 ${REPO}/src/richenum
	${POETRY} run pylint --rcfile=${REPO}/pylint.rc ${REPO}/src/richenum

test: clean
	${POETRY} run pytest

build:
	${POETRY} build