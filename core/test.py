import pandas as pd
import requests
import csv
import json
# import boto3
# import base64
import re

#import from repo
from home.ec2-user.projects.sea_to_hnl_flight_prices.helpers import awshelpers

from datetime import datetime
from pandas import json_normalize
from botocore.exceptions import ClientError

#Get secrets from secrets manager
# def get_secret_value(name, version=None):
#     secrets_client = boto3.client("secretsmanager")
#     kwargs = {'SecretId': name}
#     if version is not None:
#         kwargs['VersionStage'] = version
#     response = secrets_client.get_secret_value(**kwargs)
#     secret_string = response['SecretString']
#     secret_value_unstripped = secret_string.split(':')[1]
#     secret_value = re.sub('"|}','',secret_value_unstripped)

#     return secret_value

#Vars
now = datetime.now()
currenttime = now.strftime('%Y-%m-%d_%I%M%p')

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
directory = 'C:\\AWS\\test_outputs\\'
csv_name = currenttime+'_test.csv'
csv_path = directory+csv_name

f = open(csv_path, "w")
f.write(response.text)
f.close()
print('Wrote to local csv')

#Write to S3
# s3 = boto3.resource('s3')   
# s3.Bucket('farin-prod-test').upload_file(csv_path,'test/'+csv_name)
awshelpers.write_to_s3('farin-prod-test/test/',csv_path,csv_name)
print('Wrote to S3')


