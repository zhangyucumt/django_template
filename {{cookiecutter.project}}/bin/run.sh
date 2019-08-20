#!/usr/bin/env bash
base_dir=/usr/src/{{cookiecutter.project}}/

mode=${MODE}
env=${APP_ENV}
log_level=${LOG_LEVEL}
queue=${QUEUE}

echo env=${APP_ENV}
echo mode=${MODE}
echo log_level=${LOG_LEVEL}
echo queue=${QUEUE}

export cpus_num=`cat /proc/cpuinfo | grep "processor" |wc -l`

if [ "${mode}" == "api" ]; then
    gunicorn {{cookiecutter.project}}.config.wsgi \
        -b 0.0.0.0:{{cookiecutter.port}} \
        -w $((${cpus_num}*2+1)) \
        -t 50 \
        --log-level ${log_level} \
        --max-requests 200 \
        --keep-alive 30

elif [ "${mode}" == "worker" ]; then
    celery -A {{cookiecutter.project}}.config.celery_app worker \
        -Q ${queue} \
        -l ${log_level} \
        --concurrency $((${cpus_num}*2+1))
elif [ "${mode}" == "beat" ]; then
    celery -A {{cookiecutter.project}}.config.celery_app beat -l ${log_level}
fi
