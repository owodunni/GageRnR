init:
	pip3 install -r requirements.txt

lint:
	flake8 . --count --statistics

tests:
	pytest

build:
	python3 setup.py sdist bdist_wheel

install:
	python3 setup.py install

clean:
	rm -rf build
	rm -rf dist

check:
	twine check dist/*