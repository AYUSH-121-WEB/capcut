#!/bin/bash
python manage.py migrate
gunicorn social_project.wsgi
