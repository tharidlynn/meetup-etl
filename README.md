## ETL Meetup Events

This project consists of 4 steps:

1. Get the Meetup events from [official API](https://www.meetup.com/meetup_api/) and load into PostgreSQL
2. Create our data warehouse and perform ETL
3. Automate ETL with Apache Airflow 
4. Set up dashboard and SQL analytics


### 1. Get the Meetup events and load into PostgreSQL

<img src="./img/meetup-erd.png" alt="meetup-erd" title="meetup-erd" width="400" height="600" />


1. Modify your environments in `api/.env`
2. Run `cd api && ./init.sh`

### 2. Create our data warehouse and perform batching ETL 

<img src="./img/meetup-dwh.png" alt="meetup-dwh" title="meetup-dwh" width="400" height="600" />

1. In `dwh/setup/export_db.sql`, specify the date range in the `WHERE` clause so that we can experiment on incremental load
2. Run `cd dwh && ./etl.sh`

Note: There are some duplicate rows but the constraint of unique id automatically solves that problem!

```
-- verify that there are some duplicate rows

SELECT 
	COUNT(*), id
FROM staging."event"
GROUP BY
	id
HAVING 
	COUNT(*) > 1`
```

### 3. Incremental load with Apache Airflow 

<img src="./img/meetup-dag.png" alt="meetup-dag" title="meetup-dag" />


1. Copy every file in `meetup_dags` folder to your Airflow dag 
2. Create the `sql_dwh_path` variable in Airflow UI and point that to your sql directory, e.g. `/Users/john/airflow/dags/sql`
3. Create 2 connections in Airflow UI: `postgres_oltp` and `postgres_dwh`
```
{
   "conn_id":"postgres_oltp",
   "conn_type":"postgres",
   "host":"localhost",
   "port":5432,
   "schema":"meetup",
   "login":"john",
   "password":""
}
 
{
   "conn_id":"postgres_dwh",
   "conn_type":"postgres",
   "host":"localhost",
   "port":5432,
   "schema":"dwh",
   "login":"dwh_owner",
   "password":"dwh_owner"
}
```
4. Set up airflow pool to limit the execution parallelism `'postgres_dwh': 10`
5. Start our DAG 
6. Now, Airflow will start performing incremental loads

<img src="./img/meetup-check-quality.png" alt="meetup-check-quality" title="meetup-check-quality" />

_With the data-quality-check operator, we can guarantee that every row has been inserted into dwh._

### 4. Setup Dashboard, OLAP and analytics

#### Dashboard
I decided to use [Metabase](https://metabase.com) as the BI tool because it is an open source Business Intelligence server. You can click thumbnail below to see the demo video.

[![meetup-dashboard](https://github.com/tharid007/meetup-etl/blob/master/img/meetup-dashboard-screenshot.png?raw=true)](https://vimeo.com/352247420 "Meetup Dashboard - Click to Watch!")

#### Jupyter notebook

1. `sql.ipynb`: SQL analytics including OLAP and window functions such as:

```

WITH cte AS (SELECT 
    g.name AS group_name,
    f.yes_rsvp_count,
    CASE 
        WHEN yes_rsvp_count > LAG(f.yes_rsvp_count, 1) OVER (
        PARTITION BY g.name
        ORDER BY f.event_date
    ) THEN 1 ELSE 0 
    END AS better
FROM 
    dwh.fact_event f
    LEFT JOIN dwh.dim_group g ON f.group_key = g.group_key
    LEFT JOIN dwh.dim_event e ON f.event_key = e.event_key
)

SELECT 
    group_name,
    COUNT(*) AS total_events,
    SUM(better) AS total_better,
    SUM(better)::Float / COUNT(*)::Float AS better_percentage
FROM
    cte
GROUP BY
    group_name
ORDER BY 
    SUM(better)::Float / COUNT(*)::Float DESC;

```

2. `dataframe.ipynb`: example of using Pandas with Meetup events such as:

```
group = pd.read_csv('dwh/data/group.export.csv')
cat = pd.read_csv('dwh/data/category.export.csv')
event = pd.read_csv('dwh/data/event.export.csv')

event.sort_values('yes_rsvp_count', ascending=False)[['name', 'group_name', 'yes_rsvp_count']].head(10)

event.groupby('group_name').agg({'yes_rsvp_count': ['sum', 'min', 'max', 'mean'], 'group_name': 'count'})

```




