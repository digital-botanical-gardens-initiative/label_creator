import requests
import os
import pandas as pd
#Variables of the first window (generate from scratch)
username = os.environ.get("username")
password = os.environ.get("password")
number = int(os.environ.get("number"))
location = os.environ.get("location")
storage = os.environ.get("storage")
parambig1 = os.environ.get("parambig1")
paramsmall11 = os.environ.get("paramsmall11")
paramsmall21 = os.environ.get("paramsmall21")
#Variables of the second window (from existing)
number_ext = os.environ.get("number_ext")
number_inj = os.environ.get("number_inj")
parambig2 = os.environ.get("parambig2")
paramsmall12 = os.environ.get("paramsmall12")
paramsmall22 = os.environ.get("paramsmall22")
file_path = os.environ.get("file_path")
df = pd.read_csv(file_path, header=None)

#Create template dataframe to reserve labels
row_data = {'DBGI_SPL_ID': '',
            'Reserved': 'T',
            'BG': location,
            'inaturalist_id': '',
            'Comment': '',
            'QR': '',
            'sample_location': storage,
            'user_created': '',
            'date_created': '',
            'user_updated': '',
            'date_updated': ''}

template = pd.DataFrame([row_data for _ in range(number)], columns=['DBGI_SPL_ID',
                                 'Reserved',
                                 'BG',
                                 'inaturalist_id',
                                 'Comment',
                                 'QR',
                                 'sample_location',
                                 'user_created',
                                 'date_created',
                                 'user_updated',
                                 'date_updated'])

# Define the Directus base URL
base_url = 'http://directus.dbgi.org'

# Define the login endpoint URL
login_url = base_url + '/auth/login'
# Create a session object for making requests
session = requests.Session()
# Send a POST request to the login endpoint
response = session.post(login_url, json={'email': username, 'password': password})
data = response.json()['data']
access_token = data['access_token']
refresh_token = data['refresh_token']
DBGI_SPL_ID = 'DBGI_SPL_ID'
params = {'sort[]': f'-{DBGI_SPL_ID}'}
collection_url = base_url + '/items/samples'
response = session.get(collection_url, params=params)
last_value = response.json()['data'][0][DBGI_SPL_ID]

last_number = int(last_value.split('_')[1])
first_number = last_number + 1

values = ['dbgi_{:06d}'.format(first_number + i) for i in range(number)]

# Write the values to a CSV file
df = pd.DataFrame({'dbgi_codes': values})
df.to_csv('new_codes.csv', index=False)