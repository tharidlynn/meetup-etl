DROP TABLE IF EXISTS dwh.dim_date CASCADE;
DROP TABLE IF EXISTS dwh.dim_time CASCADE;

CREATE TABLE dwh.dim_date (
    date_pk      DATE NOT NULL PRIMARY KEY,
    year          INTEGER NOT NULL,
    month         INTEGER NOT NULL,
    month_name    VARCHAR(32) NOT NULL,
    day_of_month  INTEGER NOT NULL,
    day_of_year   INTEGER NOT NULL,
    week_day_name VARCHAR(32) NOT NULL,
    week          INTEGER NOT NULL,
    fmt_datum     VARCHAR(20) NOT NULL,
    quarter       VARCHAR(2) NOT NULL,
    year_quarter  VARCHAR(7) NOT NULL,
    year_month    VARCHAR(7) NOT NULL,
    year_week     VARCHAR(7) NOT NULL,
    month_start   DATE NOT NULL,
    month_end     DATE NOT NULL
);

CREATE TABLE dwh.dim_time (
    time_pk    TIME NOT NULL PRIMARY KEY,
    time_of_day  VARCHAR(5) NOT NULL,
    hour         INTEGER NOT NULL,
    minute       INTEGER NOT NULL,
    daytime_name VARCHAR(7) NOT NULL,
    day_night    VARCHAR(5) NOT NULL
);


INSERT INTO dwh.dim_date(
    date_pk,
    year,
    month,
    month_name,
    day_of_month,
    day_of_year,
    week_day_name,
    week,
    fmt_datum,
    quarter,
    year_quarter,
    year_month,
    year_week,
    month_start,
    month_end
)
SELECT
	datum AS date_pk,
	EXTRACT(YEAR FROM datum) AS year,
	EXTRACT(MONTH FROM datum) AS month,
	-- Localized month name
	to_char(datum, 'TMMonth') AS month_name,
	EXTRACT(DAY FROM datum) AS day_of_month,
	EXTRACT(doy FROM datum) AS day_of_year,
	-- Localized weekday
	to_char(datum, 'TMDay') AS week_day_name,
	-- ISO calendar week
	EXTRACT(week FROM datum) AS week,
	to_char(datum, 'dd. mm. yyyy') AS fmt_datum,
	'Q' || to_char(datum, 'Q') AS quarter,
	to_char(datum, 'yyyy/"Q"Q') AS year_quarter,
	to_char(datum, 'yyyy/mm') AS year_month,
	-- ISO calendar year and week
	to_char(datum, 'iyyy/IW') AS year_week,
	-- Start and end of the month of this date
	datum + (1 - EXTRACT(DAY FROM datum))::INTEGER AS month_start,
	(datum + (1 - EXTRACT(DAY FROM datum))::INTEGER + '1 month'::INTERVAL)::DATE - '1 day'::INTERVAL AS month_end
FROM (
	-- There are 3 leap years in this range, so calculate 365 * 10 + 3 records
	SELECT day::date AS datum
    FROM generate_series('2001-01-01'::timestamp, '2021-12-31'::timestamp, '1 day'::interval) AS day
     ) DQ
ORDER BY 1;


INSERT INTO dwh.dim_time ( 
    time_pk,
    time_of_day,
    hour,
    minute,
    daytime_name,
    day_night
) 
SELECT minute as time_pk,
    to_char(minute, 'hh24:mi') AS time_of_day,
	-- Hour of the day (0 - 23)
	EXTRACT(HOUR FROM minute) AS hour, 
	-- Minute of the day (0 - 1439)
	EXTRACT(HOUR FROM minute)*60 + EXTRACT(minute FROM minute) AS minute,
	-- Names of day periods
	CASE WHEN to_char(minute, 'hh24:mi') BETWEEN '06:00' AND '08:29'
		THEN 'Morning'
	     WHEN to_char(minute, 'hh24:mi') BETWEEN '08:30' AND '11:59'
		THEN 'AM'
	     WHEN to_char(minute, 'hh24:mi') BETWEEN '12:00' AND '17:59'
		THEN 'PM'
	     WHEN to_char(minute, 'hh24:mi') BETWEEN '18:00' AND '22:29'
		THEN 'Evening'
	     ELSE 'Night'
	END AS daytime_name,
	-- Indicator of day or night
	CASE WHEN to_char(minute, 'hh24:mi') BETWEEN '07:00' AND '19:59' THEN 'Day'
	     ELSE 'Night'
	END AS day_night
FROM (SELECT '0:00'::TIME + (m || ' minutes')::INTERVAL AS minute
	FROM generate_series(0,1439) AS m
     ) DQ
ORDER BY 1