COPY (SELECT
    created, duration, id, name, rsvp_limit, date_in_series_pattern, status, 
    time, local_date, local_time, updated,utc_offset, waitlist_count, yes_rsvp_count, venue_id ,
    venue_name, venue_lat, venue_lon, venue_repinned, venue_address_1, venue_city,
    venue_country, venue_localized_country_name, group_created, group_name, group_id ,
    group_join_mode, group_lat, group_lon, group_urlname, group_who, group_localized_location,
    group_state, group_country, group_region, group_timezone, link, description, visibility
    FROM event WHERE local_date < '2019-07-25'::DATE)
TO '/Users/john/Desktop/master/meetup/dwh/data/event.export.csv' (FORMAT CSV, HEADER);


COPY (SELECT
    score, id, name, status, link, urlname, description, created, city, 
    untranslated_city, country, localized_country_name, localized_location,
    state, join_mode, visibility, lat, lon ,members, organizer_id, organizer_name, 
    organizer_bio,timezone, category_id, category_name
    FROM "group" WHERE to_timestamp(created)::DATE < '2019-07-25'::DATE)
TO '/Users/john/Desktop/master/meetup/dwh/data/group.export.csv' (FORMAT CSV, HEADER);


COPY category TO '/Users/john/Desktop/master/meetup/dwh/data/category.export.csv' (FORMAT CSV, HEADER);
