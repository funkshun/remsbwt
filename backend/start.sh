#!/bin/sh

pip install --upgrade pip
pip install --no-cache -r /remsbwt/requirements.txt

gunicorn 'app:get_app()' -c /remsbwt/conf/gunicorn_conf.py --reload

