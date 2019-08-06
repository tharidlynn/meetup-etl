import os
import datetime

time_now = str(datetime.datetime.now())

log_file = 'logs/logging.log'
tmp_dir = os.path.join(os.getcwd(), 'tmp')
data_dir = os.path.join(os.getcwd(), 'data')

tmp_group_filename = '{dir}/output_group_{date}.csv'.format(dir=tmp_dir, date=time_now)
tmp_event_filename = '{dir}/output_event_{date}.csv'.format(dir=tmp_dir, date=time_now)
tmp_category_filename = '{dir}/output_category_{date}.csv'.format(dir=tmp_dir, date=time_now)

data_group_filename = os.path.join(data_dir, 'group.csv')
data_event_filename = os.path.join(data_dir, 'event.csv')
data_category_filename = os.path.join(data_dir, 'category.csv')