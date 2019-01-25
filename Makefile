integration_test:
	cd example && python ./manage.py test

unit_test:
	pytest --cov=graphene_django_actions --cov-report term-missing tests/

test: integration_test unit_test

format:
	black --exclude venv .

build:
	python setup.py sdist bdist_wheel

publish:
	python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*