test:
	pytest --cov=graphene_django_actions --cov-report term-missing tests/

format:
	black --exclude venv .

build:
	python setup.py sdist bdist_wheel

publish:
	python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*