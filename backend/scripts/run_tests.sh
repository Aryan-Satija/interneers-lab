#!/bin/bash

set -e 
set -o pipefail 

echo "Activating virtual environment :-"
source venv/scripts/activate

echo "Installing backend dependencies :-"
pip install -r requirements.txt

echo "Starting MongoDB using docker :-"
docker compose up -d mongodb

echo "Waiting for MongoDB to be ready :-"
until curl -s localhost:27018 > /dev/null; do
    sleep 0.5
done

echo "Running tests :-"
python manage.py test product.tests.integration.test_product_apis

echo "All tests passed"

echo "Cleaning up Docker container :-"
docker compose down
