SELECT
    score, id, name, status, link, urlname, description, created, city, 
    untranslated_city, country, localized_country_name, localized_location,
    state, join_mode, visibility, lat, lon ,members, organizer_id, organizer_name, 
    organizer_bio,timezone, category_id, category_name
FROM
    "group"
WHERE
    to_timestamp(created)::DATE = %(today_date)s ;
