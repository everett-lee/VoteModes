#!/bin/bash

export AWS_PROFILE=$1

echo 'Creating divisions table'
python3 ./dynamodb_scripts/divisions/load_divisions.py

echo 'Creating MPs table'
python3 ./dynamodb_scripts/mps/load_mps.py

echo 'Creating MPs to votes table'
python3 ./dynamodb_scripts/mpsToVotes/load_mps_to_votes.py
