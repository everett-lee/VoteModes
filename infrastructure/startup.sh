#!/bin/bash

export AWS_PROFILE=$1

echo 'Creating divisions table'
python3 ./dynamodb_scripts/divisions/load_divisions.py
echo 'Divisions table created'

echo 'Creating MPs table'
python3 ./dynamodb_scripts/mps/load_mps.py
echo 'MPs table created'
