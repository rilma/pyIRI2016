.PHONY : build coverage install smoke health test dev clean-venv

export PYTHONIOENCODING=utf-8
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

clean-venv:
	rm -rf .venv

dev:
	[ -d .venv ] || python3 -m venv .venv
	./.venv/bin/python -m pip install --upgrade pip wheel setuptools
	./.venv/bin/python -m pip install 'numpy>=1.21.5,<2.0' simple-settings beautifulsoup4 wget 'scikit-build-core' cmake ninja charset-normalizer
	bash -c 'VIRTUAL_ENV=./.venv PYTHONIOENCODING=utf-8 LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8 ./.venv/bin/python -m pip install -e .'
	./.venv/bin/python -m pip install pre-commit coverage pytest pytest-cov parameterized

build:
	[ -d .venv ] || python3 -m venv .venv
	./.venv/bin/python -m pip install --upgrade pip wheel setuptools
	./.venv/bin/python -m pip install 'numpy>=1.21.5,<2.0' simple-settings beautifulsoup4 wget 'scikit-build-core' cmake ninja
	./.venv/bin/python -m pip install --no-build-isolation 'build[uv]'
	./.venv/bin/python -m build

coverage:
	./.venv/bin/python -m pytest tests/ --cov=pyiri2016 --cov-report=term-missing --cov-report=html

install:
	[ -d .venv ] || python3 -m venv .venv
	./.venv/bin/python -m pip install --upgrade pip wheel setuptools
	./.venv/bin/python -m pip install 'numpy>=1.21.5,<2.0' simple-settings beautifulsoup4 wget 'scikit-build-core' cmake ninja
	./.venv/bin/python -m pip install .

smoke:
	./.venv/bin/python -m compileall -q pyiri2016 tests settings examples scripts

health:
	python3 --version
	gfortran --version
	cmake --version
	make smoke

test:
	./.venv/bin/python -m pytest tests/ -v --tb=short
