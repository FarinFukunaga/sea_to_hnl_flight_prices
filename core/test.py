import pandas as pd
import requests
import csv
#import json
import pytz

from datetime import datetime
from botocore.exceptions import ClientError

#import from repo
import awshelpers 

#Vars
fmt = '%Y-%m-%d_%I%M%p_pst'
now_pst = datetime.now(pytz.timezone('US/Pacific'))
currenttime = now_pst.strftime('%Y-%m-%d_%I%M%p_pst')

# now = datetime.now()
# currenttimeutc = now.strftime('%Y-%m-%d_%I%M%p_pst')
# currenttime = currenttimeutc.astimezone(pytz.timezone('US/Pacific'))

#Quandl Call Vars
database_code = 'FRED'
dataset_code = 'DEXUSEU'
return_format = 'csv'
collapse = 'daily'
start_date = '2020-01-01'
api_key_secret = awshelpers.get_secret_value('quandl_api_key')
final_url = f'https://www.quandl.com/api/v3/datasets/{database_code}/{dataset_code}/data.{return_format}?collapse={collapse}&start_date={start_date}&api_key={api_key_secret}'

#Call API
response = requests.get(final_url)
print(response.status_code)
print(response.url)

#Convert Response to CSV
directory = '/home/ec2-user/files/sea_test/'
csv_name = currenttime+'_test.csv'
csv_path = directory+csv_name
s3_bucket = 'farin-prod-test'
s3_path = 'test/'

f = open(csv_path, "w")
f.write(response.text)
f.close()
print('Wrote to local csv')

#Write to S3
awshelpers.write_to_s3(s3_bucket, csv_path, s3_path, csv_name)
print('Wrote to S3')


