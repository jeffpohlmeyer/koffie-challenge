#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
pip install gunicorn
cd koffie_frontend_challenge
pip install .