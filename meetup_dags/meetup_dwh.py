from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta
from airflow.models import Variable
from operators.dwh_operator import PostgresToPostgresOperator

import pendulum
import os

tmpl_search_path = Variable.get('sql_dwh_path')

local_tz = pendulum.timezone('Asia/Bangkok')

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2019, 7, 27, 0, 0, 0, 0, tzinfo=local_tz),
    'retries': 2,
    'retry_delay': timedelta(hours=1),
    'dagrun_timeout': timedelta(minutes=60),
    'depends_on_past': True
    }

with DAG(dag_id='meetup_warehouse', description='Load and transform data in Postgres with Airflow', 
         default_args=default_args, schedule_interval='@daily', default_view='graph', max_active_runs=1, template_searchpath=tmpl_search_path, catchup=True
) as dag:

    start_operator = DummyOperator(task_id='begin_execution')

    stage_event = PostgresToPostgresOperator(
                    sql='select_event.sql',
                    pg_table='staging.event',
                    src_postgres_conn_id='postgres_oltp',
                    dest_postgress_conn_id='postgres_dwh',
                    pg_preoperator='TRUNCATE TABLE staging.event;',
                    parameters={'today_date': '{{ ds }}'},
                    task_id='stage_event',
                    pool='postgres_dwh')

    stage_group = PostgresToPostgresOperator(
                    sql='select_group.sql',
                    pg_table='staging.group',
                    src_postgres_conn_id='postgres_oltp',
                    dest_postgress_conn_id='postgres_dwh',
                    pg_preoperator='TRUNCATE TABLE staging.group;',
                    parameters={'today_date': '{{ ds }}'},
                    task_id='stage_group',
                    pool='postgres_dwh')

    stage_category = PostgresToPostgresOperator(
                    sql='select_category.sql',
                    pg_table='staging.category',
                    src_postgres_conn_id='postgres_oltp',
                    dest_postgress_conn_id='postgres_dwh',
                    pg_preoperator=None,
                    parameters=None,
                    task_id='stage_category',
                    pool='postgres_dwh')

    start_process_dwh = DummyOperator(task_id='start_process_dwh')

    load_dim_event = PostgresOperator(
            task_id='load_dim_event',
            sql='process_event_dim.sql',
            postgres_conn_id='postgres_dwh',
            autocommit=True
            )

    load_dim_group = PostgresOperator(
            task_id='load_dim_group',
            sql='process_group_dim.sql',
            postgres_conn_id='postgres_dwh',
            autocommit=True
            )

    load_dim_venue = PostgresOperator(
            task_id='load_dim_venue',
            sql='process_venue_dim.sql',
            postgres_conn_id='postgres_dwh',
            autocommit=True
            )

    load_dim_category = PostgresOperator(
            task_id='load_dim_category',
            sql='process_category_dim.sql',
            postgres_conn_id='postgres_dwh',
            autocommit=True
            )

    load_dim_date = DummyOperator(task_id='load_dim_date')
    load_dim_time = DummyOperator(task_id='load_dim_time')

    load_fact_event = PostgresOperator(
            task_id='load_fact_event',
            sql='process_event_fact.sql',
            postgres_conn_id='postgres_dwh',
            autocommit=True
            )
            
    check_query = """
        INSERT INTO check_quality (event_source, event_target, event_date, process_ts)
        SELECT
	(SELECT
		count(*) AS total_count
	        FROM
	staging."event"), COUNT(*), '{{ ds }}'::DATE, CURRENT_TIMESTAMP
        FROM
	dwh.fact_event
        WHERE event_date = '{{ ds }}' ;
        """

    data_quality_check = PostgresOperator(
            task_id='data_quality_check',
            sql=check_query,
            postgres_conn_id='postgres_dwh',
            autocommit=True
            )

    end_operator = DummyOperator(task_id='stop_execution')

    start_operator >> [stage_event, stage_group, stage_category] >> start_process_dwh
    start_process_dwh >> [load_dim_event, load_dim_group, load_dim_venue, load_dim_category, load_dim_date, load_dim_time] >> load_fact_event
    load_fact_event >> data_quality_check >> end_operator
