.PHONY : build coverage install smoke health test test-examples demo-plots dev dev-plotting clean-venv

export PYTHONIOENCODING=utf-8
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

clean-venv:
	rm -rf .venv

dev:
	[ -d .venv ] || python3 -m venv .venv
	./.venv/bin/python -m pip install --upgrade pip wheel setuptools
	./.venv/bin/python -m pip install 'numpy>=2.0' simple-settings beautifulsoup4 wget 'scikit-build-core' cmake ninja charset-normalizer
	bash -c 'VIRTUAL_ENV=./.venv PYTHONIOENCODING=utf-8 LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8 ./.venv/bin/python -m pip install -e .'
	./.venv/bin/python -m pip install pre-commit coverage pytest pytest-cov parameterized

dev-plotting:
	[ -d .venv ] || python3 -m venv .venv
	./.venv/bin/python -m pip install --upgrade pip wheel setuptools
	./.venv/bin/python -m pip install 'numpy>=2.0' simple-settings beautifulsoup4 wget 'scikit-build-core' cmake ninja charset-normalizer
	bash -c 'VIRTUAL_ENV=./.venv PYTHONIOENCODING=utf-8 LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8 ./.venv/bin/python -m pip install -e .[plotting]'
	./.venv/bin/python -m pip install pre-commit coverage pytest pytest-cov parameterized

build:
	[ -d .venv ] || python3 -m venv .venv
	./.venv/bin/python -m pip install --upgrade pip wheel setuptools
	./.venv/bin/python -m pip install 'numpy>=2.0' simple-settings beautifulsoup4 wget 'scikit-build-core' cmake ninja
	./.venv/bin/python -m pip install --no-build-isolation 'build[uv]'
	./.venv/bin/python -m build

coverage:
	./.venv/bin/python -m pytest tests/ --cov=pyiri2016 --cov-report=term-missing --cov-report=html

install:
	[ -d .venv ] || python3 -m venv .venv
	./.venv/bin/python -m pip install --upgrade pip wheel setuptools
	./.venv/bin/python -m pip install 'numpy>=2.0' simple-settings beautifulsoup4 wget 'scikit-build-core' cmake ninja
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

test-examples:
	@echo "Testing non-plotting examples..."
	./.venv/bin/python examples/example01.py > /dev/null && echo "✓ example01.py passed" || echo "✗ example01.py failed"
	./.venv/bin/python examples/example02.py > /dev/null && echo "✓ example02.py passed" || echo "✗ example02.py failed"
	@echo "Testing plotting examples (with headless display)..."
	MPLBACKEND=Agg ./.venv/bin/python examples/iri1DExample01.py > /dev/null && echo "✓ iri1DExample01.py passed" || echo "✗ iri1DExample01.py failed"
	MPLBACKEND=Agg ./.venv/bin/python examples/iri1DExample01b.py > /dev/null && echo "✓ iri1DExample01b.py passed" || echo "✗ iri1DExample01b.py failed"
	MPLBACKEND=Agg ./.venv/bin/python examples/iri1DExample02.py > /dev/null && echo "✓ iri1DExample02.py passed" || echo "✗ iri1DExample02.py failed"
	MPLBACKEND=Agg ./.venv/bin/python examples/iri1DExample08.py > /dev/null && echo "✓ iri1DExample08.py passed" || echo "✗ iri1DExample08.py failed"
	MPLBACKEND=Agg ./.venv/bin/python scripts/iri2DExample01.py > /dev/null && echo "✓ iri2DExample01.py passed" || echo "✗ iri2DExample01.py failed"
	MPLBACKEND=Agg ./.venv/bin/python scripts/iri2DExample02.py > /dev/null && echo "✓ iri2DExample02.py passed" || echo "✗ iri2DExample02.py failed"

demo-plots: clean-venv
	[ -d .venv ] || python3 -m venv .venv
	./.venv/bin/python -m pip install --upgrade pip wheel setuptools
	./.venv/bin/python -m pip install 'numpy>=2.0' simple-settings beautifulsoup4 wget 'scikit-build-core' cmake ninja charset-normalizer	bash -c 'VIRTUAL_ENV=./.venv PYTHONIOENCODING=utf-8 LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8 ./.venv/bin/python -m pip install --no-cache-dir --force-reinstall -e .[plotting]'
	./.venv/bin/python -m pip install pre-commit coverage pytest pytest-cov parameterized
	@echo "Generating and saving plotting examples to figures/ directory..."
	MPLBACKEND=Agg ./.venv/bin/python examples/demo_save_plots.py
