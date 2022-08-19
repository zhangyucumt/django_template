FROM registry.cn-shanghai.aliyuncs.com/zhangyucumt/python:3.8-bullseye

ENV APP_ENV prd
ENV DJANGO_SETTINGS_MODULE {{cookiecutter.project}}.config.settings

ADD requirements.txt /srv/
WORKDIR /srv/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /srv/

EXPOSE {{cookiecutter.port}}

CMD ["sh", "-c", "gunicorn {{cookiecutter.project}}.config.wsgi -b 0.0.0.0:{{cookiecutter.port}} -w 10 -t 50 --log-level info --max-requests 200 --keep-alive 30"]
