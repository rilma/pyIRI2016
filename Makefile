
build:
	ansible-playbook .ansible/poetry.yaml
	poetry install
	cd ./source && poetry run f2py -m iri2016 -c iriwebg.for irisub.for irifun.for iritec.for iridreg.for igrf.for cira.for iriflip.for skip: dfridr
