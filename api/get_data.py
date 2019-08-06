import os
import logging

import time
import shutil 

from meetup.meetup_api import extract_events, extract_groups, extract_categories
from meetup.save_to_csv import save_categories_to_csv, save_groups_to_csv, save_events_to_csv
from meetup.meetup_config import *

logger = logging.getLogger(__name__)

def extract_meetup_data():
    events = extract_events()
    groups = extract_groups()
    categories = extract_categories()

    return events, groups, categories


def save_data_to_csv(event, group, category):
    save_events_to_csv(event, tmp_event_filename)
    save_groups_to_csv(group, tmp_group_filename)
    save_categories_to_csv(category, tmp_category_filename)

    # keep the original tmp file and copy new file 
    shutil.copyfile(tmp_group_filename, data_group_filename)
    shutil.copyfile(tmp_event_filename, data_event_filename)
    shutil.copyfile(tmp_category_filename, data_category_filename)

    return 'Successfully save Meetup data'


def main():
    assert os.environ.get('API_KEY') != None
    
    try:
        os.remove(log_file)
    except OSError:
        pass

    logging.basicConfig(filename=log_file, format='%(funcName)s: %(asctime)s %(module)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
     level=logging.DEBUG)
    
    event, group, category = extract_meetup_data()
    
    save_data_to_csv(event, group, category)
    

if __name__ == '__main__':
    start_time = time.time()

    main()

    print(f'finish in {time.time() - start_time}')