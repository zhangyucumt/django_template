### Usage
```makefile
pylint:
    flake8 {{cookiecutter.project}} --max-line-length=120

pytest:
    pytest unitest

dev_requirements:
    pip install -r requirements_dev.txt

requirements:
    pip install -r requirements.txt

server:
    gunicorn {{cookiecutter.project}}.config.wsgi -b 0.0.0.0:8061 --reload --log-level debug -w 1

clean_pyc:
    @find . -name '*.pyc' -delete
```
