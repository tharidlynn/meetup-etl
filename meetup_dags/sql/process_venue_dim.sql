INSERT INTO dwh.dim_venue (id, name, lat, lon, repinned, address, city, country)
    SELECT
        e.venue_id, e.venue_name, e.venue_lat, e.venue_lon, e.venue_repinned, e.venue_address_1, e.venue_city, e.venue_country
    FROM
        staging.event e
    WHERE e.venue_id IS NOT NULL
ON CONFLICT (id) DO NOTHING;