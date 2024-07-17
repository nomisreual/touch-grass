#!/usr/bin/env bash

coverage run --source='.' --omit config/*,utils/*,manage.py manage.py test
# coverage html
coverage report
