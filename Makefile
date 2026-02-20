.PHONY : build coverage install smoke health test dev

export PYTHONIOENCODING=utf-8
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

dev:
	[ -d .venv ] || python3 -m venv .venv
	./.venv/bin/python -m pip install --upgrade pip 'setuptools>=60,<70' wheel charset-normalizer 'numpy>=1.21.5,<2.0' simple-settings beautifulsoup4 wget
	./.venv/bin/python setup.py develop
	./.venv/bin/python -m pip install pre-commit coverage parameterized

build:
	[ -d .venv ] || python3 -m venv .venv
	./.venv/bin/python -m pip install --upgrade pip 'setuptools>=60,<70' wheel charset-normalizer 'numpy>=1.21.5,<2.0' simple-settings beautifulsoup4 wget
	./.venv/bin/python setup.py sdist bdist_wheel

coverage:
	uv run coverage report

install:
	[ -d .venv ] || python3 -m venv .venv
	./.venv/bin/python -m pip install --upgrade pip 'setuptools>=60,<70' wheel charset-normalizer 'numpy>=1.21.5,<2.0' simple-settings beautifulsoup4 wget
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
