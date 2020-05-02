.PHONY: test clean setup lint

lint:
	./bin/flake8 radiotalk-dl.py

test:
	./bin/python tests.py

clean:
	find . -name "*.py[co]" -delete
	rm -rf __pycache__ .mypy_cache

setup:
	python3 -m venv .
	./bin/pip install -r requirements.txt
