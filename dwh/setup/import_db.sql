COPY staging.event FROM '/Users/john/Desktop/master/meetup/dwh/data/event.export.csv' (FORMAT CSV, HEADER);

COPY staging.group FROM '/Users/john/Desktop/master/meetup/dwh/data/group.export.csv' (FORMAT CSV, HEADER);

COPY staging.category FROM '/Users/john/Desktop/master/meetup/dwh/data/category.export.csv' (FORMAT CSV, HEADER);
