.PHONY : build coverage install test


build:
	cd ./source && poetry run f2py -m iri2016 -c iriwebg.for irisub.for irifun.for iritec.for iridreg.for igrf.for cira.for iriflip.for skip: dfridr

coverage:
	poetry run coverage report

install:
	ansible-playbook .ansible/poetry.yaml
	poetry install

test:
	poetry run coverage run \
		--source=. \
		--module unittest discover \
		--start-directory . \
		--pattern test_*.py \
		--verbose
