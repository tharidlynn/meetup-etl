#!/usr/bin/env bash
source .env
python get_data.py && python insert_to_db.py

