import pandas as pd
import fsspec
#import requests
import json
import csv
import pytz

from amadeus import Client, ResponseError
from datetime import datetime
from botocore.exceptions import ClientError

#import from repo
import awshelpers 

amadeus = Client(
    client_id=awshelpers.get_secret_value('amadeus_api_key'),
    client_secret=awshelpers.get_secret_value('amadeus_api_secret')
)

#Vars
fmt = '%Y-%m-%d_%I%M%p_pst'
now_pst = datetime.now(pytz.timezone('US/Pacific'))
currenttime = now_pst.strftime('%Y-%m-%d_%I%M%p_pst')

#Amadeus Call Vars
origin_code = 'SEA'
destination_code = 'HNL'
departure_date = '2021-12-01'
num_adults = 1

#Call API

response = amadeus.shopping.flight_offers_search.get(
    originLocationCode=origin_code,
    destinationLocationCode=destination_code,
    departureDate=departure_date,
    adults=num_adults)

#Convert Response to CSV
directory = '/home/ec2-user/files/sea_test/'
csv_name = currenttime+'_am_test.csv'
csv_path = directory+csv_name
s3_bucket = 'farin-prod-test'
s3_path = 'test/amadeus/'

json_data = json.loads(response.result)
df = pd.DataFrame.from_dict(json_data, orient='index')
print(df)

# f = open(csv_path, "w")
# f.write(df.to_csv())
# f.close()
# print('Wrote to local csv')

#Write to S3
# awshelpers.write_to_s3(s3_bucket, csv_path, s3_path, csv_name)
# print('Wrote to S3')
