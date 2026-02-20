.PHONY : build coverage install smoke health test


build:
	cd ./source && poetry run f2py -m iri2016 -c iriwebg.for irisub.for irifun.for iritec.for iridreg.for igrf.for cira.for iriflip.for skip: dfridr

coverage:
	poetry run coverage report

install:
	ansible-playbook .ansible/poetry.yaml
	poetry install

smoke:
	python -m compileall -q pyiri2016 tests settings examples scripts

health:
	python --version
	poetry --version
	gfortran --version
	make smoke

test:
	poetry run coverage run \
		--source=. \
		--module unittest discover \
		--start-directory . \
		--pattern test*.py \
		--verbose
