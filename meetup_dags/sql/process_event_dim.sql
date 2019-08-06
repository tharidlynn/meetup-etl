INSERT INTO dwh.dim_event (id, name, description, link)
    SELECT
        e.id, e.name, e.description, e.link
    FROM
        staging.event e
ON CONFLICT (id) DO NOTHING;