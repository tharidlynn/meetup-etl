import os
import logging
import requests

API_KEY = os.getenv('API_KEY')

logger = logging.getLogger(__name__)


def extract_categories():
    url = 'https://api.meetup.com/2/categories?key={api_key}&page=50'\
		   .format(api_key=API_KEY)
    cat = requests.get(url).json()['results']

    return cat

def extract_groups():
    url = 'https://api.meetup.com/find/groups?key={api_key}&country={country}&photo-host=public&page=250'\
		   .format(api_key=API_KEY, country='th')
    res = requests.get(url).json()
    groups = [group for group in res]
    
    return groups

def extract_groupnames():
    url = 'https://api.meetup.com/find/groups?key={api_key}&country={country}&photo-host=public&page=250'\
		   .format(api_key=API_KEY, country='th')
    groups = requests.get(url).json()
    groups_names = [group['urlname'] for group in groups]
    
    return groups_names

def extract_events(status='past'):
    data = []
    groups_names = extract_groupnames()

    for i, url_name in enumerate(groups_names):
        logger.info('Group {}'.format(i+1))
        event_url = 'https://api.meetup.com/{url_name}/events?key={api_key}&country={country}&photo-host=public&page=250&status={status}'\
    				.format(url_name=url_name, status=status, api_key=API_KEY, country='th')
        events = requests.get(event_url).json()
        if len(events) == 0:
            logger.info('{url_name} doesn\'t have any events'.format(url_name=url_name))
        data.append(events)
    
    return data