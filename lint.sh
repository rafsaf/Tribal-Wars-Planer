#!/bin/bash
echo "export requirements.txt"
poetry export -o requirements.txt
echo "autoflake"
autoflake --recursive --in-place  \
        --remove-unused-variables \
        --remove-all-unused-imports  \
        --ignore-init-module-imports \
        base rest_api tribal_wars_planer utils
echo "black"
black base rest_api tribal_wars_planer utils
echo "isort"
isort base rest_api tribal_wars_planer utils
echo "flake8"
flake8 base rest_api tribal_wars_planer utils