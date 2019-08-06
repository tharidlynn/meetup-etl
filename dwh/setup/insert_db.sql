INSERT INTO dwh.dim_category (id, name)
    SELECT
        c.id, c.name
    FROM 
        staging.category c
ON CONFLICT (id) DO NOTHING;

INSERT INTO dwh.dim_event (id, name, description, link)
    SELECT
        e.id, e.name, e.description, e.link
    FROM
        staging.event e
ON CONFLICT (id) DO NOTHING;

INSERT INTO dwh.dim_group (id, name, description, link, created, category, organizer)
    SELECT
        g.id, g.name, g.description, g.link, g.created, g.category_name, g.organizer_name
    FROM
        staging.group g
ON CONFLICT (id) DO NOTHING;


INSERT INTO dwh.dim_venue (id, name, lat, lon, repinned, address, city, country)
    SELECT
        e.venue_id, e.venue_name, e.venue_lat, e.venue_lon, e.venue_repinned, e.venue_address_1, e.venue_city, e.venue_country
    FROM
        staging.event e
    WHERE e.venue_id IS NOT NULL
ON CONFLICT (id) DO NOTHING;

INSERT INTO dwh.fact_event 
    (event_key, group_key, date_key, time_key, category_key, venue_key,
    event_date, event_time, rsvp_limit, yes_rsvp_count, waitlist_count)
SELECT 
    dim_event.event_key, dim_group.group_key, d.date_pk, t.time_pk, dim_category.category_key, dim_venue.venue_key,
	staging_event.local_date, staging_event.local_time, staging_event.rsvp_limit, staging_event.yes_rsvp_count, staging_event.waitlist_count
FROM 
    staging.event staging_event    
INNER JOIN dwh.dim_date d ON d.date_pk = staging_event.local_date
INNER JOIN dwh.dim_time t ON t.time_pk = staging_event.local_time
LEFT JOIN dwh.dim_event dim_event ON dim_event.id = staging_event.id
LEFT JOIN dwh.dim_group dim_group ON dim_group.id = staging_event.group_id
LEFT JOIN dwh.dim_category dim_category ON dim_category.name = dim_group.category
LEFT JOIN dwh.dim_venue dim_venue ON dim_venue.id = staging_event.venue_id
ON CONFLICT (event_key) DO NOTHING;







