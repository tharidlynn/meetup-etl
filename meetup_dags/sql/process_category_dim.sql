INSERT INTO dwh.dim_category (id, name)
    SELECT
        c.id, c.name
    FROM 
        staging.category c
ON CONFLICT (id) DO NOTHING;