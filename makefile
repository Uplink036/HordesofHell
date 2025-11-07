init: 
	pip install -r requirements.txt 

tests: 
	pytest tests 

.PHONY: init test 
