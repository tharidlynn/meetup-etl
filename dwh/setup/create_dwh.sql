\c dwh;

DROP TABLE  IF EXISTS staging.event CASCADE;
DROP TABLE IF EXISTS staging.group CASCADE;
DROP TABLE IF EXISTS staging.category CASCADE;

DROP TABLE IF EXISTS dwh.fact_event CASCADE;
DROP TABLE IF EXISTS dwh.dim_event CASCADE;
DROP TABLE IF EXISTS dwh.dim_group CASCADE;
DROP TABLE IF EXISTS dwh.dim_venue CASCADE;
DROP TABLE IF EXISTS dwh.dim_category CASCADE;




CREATE TABLE staging.event (
    created    INTEGER,
    duration   INTEGER,
    id         VARCHAR(50) NOT NULL,
    name     TEXT NOT NULL,
    rsvp_limit INTEGER,
    date_in_series_pattern BOOLEAN,
    status   VARCHAR(10) DEFAULT 'past',
    time     INTEGER NOT NULL,
    local_date  DATE NOT NULL,
    local_time TIME NOT NULL,
    updated INTEGER,
    utc_offset INTEGER NOT NULL,
    waitlist_count INTEGER NOT NULL,
    yes_rsvp_count  INTEGER NOT NULL,
    venue_id  INTEGER,
    venue_name TEXT,
    venue_lat FLOAT,
    venue_lon FLOAT,
    venue_repinned BOOLEAN,
    venue_address_1 TEXT,
    venue_city  VARCHAR(50),
    venue_country VARCHAR(2),
    venue_localized_country_name VARCHAR(30),
    group_created  INTEGER ,
    group_name TEXT ,
    group_id  INTEGER ,
    group_join_mode VARCHAR(10),
    group_lat FLOAT,
    group_lon FLOAT,
    group_urlname TEXT,
    group_who TEXT,
    group_localized_location TEXT,
    group_state TEXT,
    group_country VARCHAR(2),
    group_region VARCHAR(6),
    group_timezone VARCHAR(20),
    link TEXT,
    description TEXT,
    visibility TEXT
);  

CREATE TABLE staging.group (
   score NUMERIC(2,1),
   id INTEGER,
   name TEXT,
   status TEXT,
   link TEXT,
   urlname TEXT,
   description TEXT,
   created INTEGER,
   city TEXT,
   untranslated_city TEXT,
   country TEXT,
   localized_country_name TEXT,
   localized_location TEXT,
   state TEXT,
   join_mode TEXT,
   visibility TEXT,
   lat FLOAT,
   lon FLOAT ,
   members INTEGER,
   organizer_id INTEGER,
   organizer_name TEXT,
   organizer_bio TEXT,
   timezone TEXT,
   category_id INTEGER,
   category_name TEXT
);

CREATE TABLE staging.category (
    id    INTEGER NOT NULL,
    name  TEXT    NOT NULL
);



CREATE TABLE dwh.dim_event(
    event_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id VARCHAR(50) NOT NULL,
    name TEXT,
    description TEXT,
    link TEXT,
    unique (id)
);

CREATE TABLE dwh.dim_group(
    group_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id INTEGER NOT NULL, 
    name TEXT,
    description TEXT, 
    link TEXT,
    created INTEGER,
    category TEXT,
    organizer TEXT,
    unique (id)
);

CREATE TABLE dwh.dim_venue(
    venue_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id  INTEGER,
    name TEXT,
    lat FLOAT,
    lon FLOAT,
    repinned BOOLEAN,
    address TEXT,
    city TEXT,
    country TEXT,
    unique (id)
);

CREATE TABLE dwh.dim_category(
    category_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id    INTEGER NOT NULL,
    name  TEXT    NOT NULL,
    unique (id)
);


CREATE TABLE dwh.fact_event(
    event_key  INTEGER NOT NULL REFERENCES dwh.dim_event (event_key),
    group_key  INTEGER NOT NULL REFERENCES dwh.dim_group (group_key),
    date_key  DATE NOT NULL REFERENCES dwh.dim_date (date_pk),
    time_key TIME NOT NULL REFERENCES dwh.dim_time (time_pk),
    category_key INTEGER NOT NULL REFERENCES dwh.dim_category (category_key),
    venue_key INTEGER REFERENCES dwh.dim_venue (venue_key),
    event_date DATE NOT NULL,
    event_time TIME NOT NULL,
    rsvp_limit INTEGER, 
    yes_rsvp_count INTEGER , 
    waitlist_count INTEGER,
    unique (event_key)
);