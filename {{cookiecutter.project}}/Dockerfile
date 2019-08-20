FROM python-37-centos7:2

ENV LOG_LEVEL info
ENV APP_ENV dev
ENV MODE api
ENV QUEUE default,action

ADD requirements.txt /usr/src/{{cookiecutter.project}}/
WORKDIR /usr/src/{{cookiecutter.project}}/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/{{cookiecutter.project}}/

COPY bin/run.sh /
RUN chmod 0755 /*.sh
CMD ["/run.sh"]
