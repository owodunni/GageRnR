init:
	pip3 install -r requirements.txt

lint:
	flake8 . --count --max-complexity=10 --max-line-length=127 --statistics

test:
	python3 tests/test.py

package:
	python3 setup.py sdist bdist_wheel

install:
	python3 setup.py install