
test-cli:
	python limber/cli/cli.py --gcp-keyfile "test key file" --gcp-project "test project"
test:
	python limber
deploy:
	terraform apply
build-pypi-package:
	python setup.py sdist bdist_wheel
deploy-to-pypi:
	python -m twine upload --config-file .pypirc -r pypi dist/*
install-locally:
	python -m pip install -e ~/git/limber/

limber-plan:
	limber plan
	terraform -chdir=terraform_plan init

tf-plan:
	terraform -chdir=terraform_plan plan -no-color

tf-apply:
	terraform -chdir=terraform_plan apply -auto-approve
