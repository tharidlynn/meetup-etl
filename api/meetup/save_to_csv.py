import csv
import datetime
import logging

logger = logging.getLogger(__name__)

def milli_epoch(epoch):
    if epoch:
        return round(epoch/1000)
    else:
        return epoch

def save_events_to_csv(data, output_events_file):
    fieldnames = ['created', 'duration', 'id', 'name', 'rsvp_limit', 'date_in_series_pattern', 'status', 'time',
                'local_date', 'local_time', 'updated', 'utc_offset', 'waitlist_count', 'yes_rsvp_count',
                'venue_id', 'venue_name', 'venue_lat', 'venue_lon', 'venue_repinned',
                'venue_address_1', 'venue_city', 'venue_country', 'venue_localized_country_name',
                'group_created', 'group_name', 'group_id', 'group_join_mode', 'group_lat', 'group_lon',
                'group_urlname', 'group_who', 'group_localized_location','group_state', 'group_country', 
                'group_region', 'group_timezone', 'link', 'description', 'visibility']

    with open(output_events_file, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
    for g in data:
        for event in g:
            try:
                with open(output_events_file, 'a') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writerow({
                                    'created': milli_epoch(event['created']) if 'created' in event else None, 
                                    'duration': event['duration'] if 'duration' in event else None,
                                    'id': event['id'], 
                                    'name': event['name'], 
                                    'rsvp_limit': event['rsvp_limit'] if 'rsvp_limit' in event else None,
                                    'date_in_series_pattern': event['date_in_series_pattern'] if 'date_in_series_pattern' in event else None,
                                    'status': event['status'] if 'status' in event else None, 
                                    'time': milli_epoch(event['time']), 
                                    'local_date': event['local_date'], 
                                    'local_time': event['local_time'],
                                    'updated': milli_epoch(event['updated']) if 'updated' in event else None, 
                                    'utc_offset': event['utc_offset'], 
                                    'waitlist_count': event['waitlist_count'], 
                                    'yes_rsvp_count': event['yes_rsvp_count'], 
                                    'venue_id': event['venue']['id'] if 'venue' in event else None,
                                    'venue_name': event['venue']['name'] if 'venue' in event else None,
                                    'venue_lat': event['venue']['lat'] if 'venue' in event else None,
                                    'venue_lon': event['venue']['lon'] if 'venue' in event else None,
                                    'venue_repinned': event['venue']['repinned'] if 'venue' in event else None,
                                    'venue_address_1': event['venue']['address_1'] if 'venue' in event and 'address_1' in event['venue'] else None,
                                    'venue_city': event['venue']['city'] if 'venue' in event else None,
                                    'venue_country': event['venue']['country'] if 'venue' in event else None,
                                    'venue_localized_country_name': event['venue']['localized_country_name'] if 'venue' in event else None,
                                    'group_created': milli_epoch(event['group']['created']), 
                                    'group_name': event['group']['name'], 
                                    'group_id': event['group']['id'], 
                                    'group_join_mode': event['group']['join_mode'], 
                                    'group_lat': event['group']['lat'],
                                    'group_lon': event['group']['lon'], 
                                    'group_urlname': event['group']['urlname'], 
                                    'group_who': event['group']['who'], 
                                    'group_localized_location': event['group']['localized_location'], 
                                    'group_state': event['group']['state'],
                                    'group_country': event['group']['country'], 
                                    'group_region': event['group']['region'], 
                                    'group_timezone': event['group']['timezone'],
                                    'link': event['link'], 
                                    'description': event['description'] if 'description' in event else None, 
                                    'visibility': event['visibility']
                                    })
            except BaseException as e:
                logger.error(str(event['group']['name']) + str(event['id']) + str(e))



def save_groups_to_csv(data, output_groups_file):
    fieldnames = ['score', 'id', 'name', 'status', 'link', 'urlname', 'description',
                'created', 'city', 'untranslated_city', 'country', 'localized_country_name', 'localized_location',
                'state', 'join_mode', 'visibility', 'lat', 'lon',
                'members', 'organizer_id', 'organizer_name', 'organizer_bio',
                'timezone', 'category_id', 'category_name']

    with open(output_groups_file, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
    for group in data:
        try:
            with open(output_groups_file, 'a') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({
                                'score': group['score'], 
                                'id': group['id'],
                                'name': group['name'], 
                                'status': group['status'], 
                                'link': group['link'],
                                'urlname': group['urlname'],
                                'description': group['description'], 
                                'created': milli_epoch(group['created']), 
                                'city': group['city'], 
                                'untranslated_city': group['untranslated_city'],
                                'country': group['country'], 
                                'localized_country_name': group['localized_country_name'], 
                                'localized_location': group['localized_location'], 
                                'state': group['state'], 
                                'join_mode': group['join_mode'],
                                'visibility': group['visibility'], 
                                'lat': group['lat'], 
                                'lon': group['lon'],
                                'members': group['members'], 
                                'organizer_id': group['organizer']['id'], 
                                'organizer_name': group['organizer']['name'],
                                'organizer_bio': group['organizer']['bio'], 
                                'timezone': group['timezone'], 
                                'category_id': group['category']['id'], 
                                'category_name': group['category']['name']
                                })
        except KeyError as e:
            logger.error(e)



def save_categories_to_csv(data, output_categories_file):
    fieldnames = ['id', 'name']

    with open(output_categories_file, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

    for category in data:
        try:
            with open(output_categories_file, 'a') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({
                                'id': category['id'], 
                                'name': category['name']
                                })
        except KeyError as e:
            logger.error(e)
