from meetup.meetup_config import data_group_filename, data_event_filename, data_category_filename

create_event_table = """CREATE TABLE event (
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
);  """

create_group_table = """
CREATE TABLE "group" (
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
"""


create_category_table = """
CREATE TABLE category (
    id    INTEGER NOT NULL,
    name  TEXT    NOT NULL
);
"""

insert_event_query = f"COPY event FROM '{data_event_filename}' DELIMITER ',' CSV HEADER;"
insert_group_query = f"COPY \"group\" FROM '{data_group_filename}' DELIMITER ',' CSV HEADER;"
insert_category_query = f"COPY category FROM '{data_category_filename}' DELIMITER ',' CSV HEADER;"

create_table_queries = [create_event_table, create_category_table, create_group_table]
insert_table_queries = [insert_event_query, insert_group_query, insert_category_query]