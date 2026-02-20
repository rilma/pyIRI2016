.PHONY : build coverage install smoke health test dev

export PYTHONIOENCODING=utf-8
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

dev:
	[ -d .venv ] || uv venv
	uv pip install --upgrade pip 'setuptools==58.2.0' wheel charset-normalizer numpy simple-settings beautifulsoup4 wget
	./.venv/bin/python setup.py develop
	uv pip install pre-commit coverage parameterized

build:
	[ -d .venv ] || uv venv
	uv pip install --upgrade pip 'setuptools==58.2.0' wheel charset-normalizer numpy simple-settings beautifulsoup4 wget
	./.venv/bin/python setup.py sdist bdist_wheel

coverage:
	uv run coverage report

install:
	[ -d .venv ] || uv venv
	uv pip install --upgrade pip 'setuptools==58.2.0' wheel charset-normalizer numpy simple-settings beautifulsoup4 wget
	./.venv/bin/python setup.py install

smoke:
	./.venv/bin/python -m compileall -q pyiri2016 tests settings examples scripts

health:
	uv --version
	python --version
	gfortran --version
	make smoke

test:
	./.venv/bin/python -m coverage run \
		--source=. \
		--module unittest discover \
		--start-directory . \
		--pattern test*.py \
		--verbose
