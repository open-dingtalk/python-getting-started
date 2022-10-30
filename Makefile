init:
	pip3 install -r requirements.txt

test:
	python3 -m unittest discover --verbose

start:
	python3 app.py

.PHONY: init test start
