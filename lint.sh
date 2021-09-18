#!/bin/bash

poetry export -o requirements.txt \
&& poetry run autoflake --remove-unused-variables --remove-all-unused-imports -r -i --ignore-init-module-imports base rest_api tribal_wars_planer utils \
&& poetry run black base rest_api tribal_wars_planer utils \
&& poetry run isort base rest_api tribal_wars_planer utils \
&& poetry run flake8 base rest_api tribal_wars_planer utils