pylint:
	flake8 genji --max-line-length=120 --exclude=genji/rpc/zmop,libs

pytest:
	pytest unitest

dev_requirements:
	pip install -r requirements_dev.txt

requirements:
	pip install -r requirements.txt

server:
	gunicorn {{cookiecutter.project}}.config.wsgi -b 0.0.0.0:{{cookiecutter.port}} --reload --log-level debug -w 1

clean_pyc:
	@find . -name '*.pyc' -delete
