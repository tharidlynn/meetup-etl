INSERT INTO dwh.dim_group (id, name, description, link, created, category, organizer)
    SELECT
        g.id, g.name, g.description, g.link, g.created, g.category_name, g.organizer_name
    FROM
        staging.group g
ON CONFLICT (id) DO NOTHING;