import requests
import os
import pandas as pd

#Variables of the first window (generate from scratch)
username = os.environ.get("username")
password = os.environ.get("password")
location = os.environ.get("location")
storage = os.environ.get("storage")
number = int(os.environ.get("number"))

# Check if username and password are set (not empty)
if username and password and location and storage and number != 0:
    parambig1 = os.environ.get("parambig1")
    paramsmall11 = os.environ.get("paramsmall11")
    paramsmall21 = os.environ.get("paramsmall21")

    # Create template dataframe to reserve labels
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

else:
    print("Username and/or password not set. The script will be ignored.")
