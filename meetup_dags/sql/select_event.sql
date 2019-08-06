SELECT
    created, duration, id, name, rsvp_limit, date_in_series_pattern, status, 
    time, local_date, local_time, updated,utc_offset, waitlist_count, yes_rsvp_count, venue_id ,
    venue_name, venue_lat, venue_lon, venue_repinned, venue_address_1, venue_city,
    venue_country, venue_localized_country_name, group_created, group_name, group_id ,
    group_join_mode, group_lat, group_lon, group_urlname, group_who, group_localized_location,
    group_state, group_country, group_region, group_timezone, link, description, visibility
FROM
    event
WHERE
    local_date = %(today_date)s ;


