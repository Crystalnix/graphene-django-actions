from setuptools import setup
import pathlib
from graphene_django_actions import __version__

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="graphene_django_actions",
    version=__version__,
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Crystalnix/graphene-django-actions",
    author="Artem Nesterenko",
    author_email="nesterenko.artyom@gmail.com",
    license="MIT",
    packages=["graphene_django_actions"],
    install_requires=["graphene_django>=2.0.0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
