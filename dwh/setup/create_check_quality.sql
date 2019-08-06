DROP TABLE  IF EXISTS check_quality;

CREATE TABLE check_quality (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    event_source INTEGER NOT NULL,
    event_target INTEGER NOT NULL,
    event_date DATE NOT NULL,
    process_ts TIMESTAMPTZ NOT NULL
)