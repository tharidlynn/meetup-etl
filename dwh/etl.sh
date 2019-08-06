#!/usr/bin/env bash

psql -f setup/create_users.sql
PGPASSWORD=dwh_owner psql -h localhost -p 5432 -U dwh_owner -d dwh -f setup/create_dim_datetime.sql
PGPASSWORD=dwh_owner psql -h localhost -p 5432 -U dwh_owner -d dwh -f setup/create_dwh.sql
PGPASSWORD=dwh_owner psql -h localhost -p 5432 -U dwh_owner -d dwh -f setup/create_check_quality.sql

# export data
psql -d meetup -f setup/export_db.sql

# import to staging
PGPASSWORD=dwh_owner psql -h localhost -p 5432 -U dwh_owner -d dwh -f setup/import_db.sql

# insert to data warehouse
PGPASSWORD=dwh_owner psql -h localhost -p 5432 -U dwh_owner -d dwh -f setup/insert_db.sql
