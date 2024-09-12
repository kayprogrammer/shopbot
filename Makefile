ifneq (,$(wildcard ./.env))
include .env
export 
ENV_FILE_PARAM = --env-file .env

endif

run:
	python app.py

req:
	pip install -r requirements.txt

ureq:
	pip freeze > requirements.txt

mmig:
	flask db migrate
	
mig:
	flask db upgrade