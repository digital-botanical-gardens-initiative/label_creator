import requests
import os
import pandas as pd

#Variables of the first window (generate from scratch)
username = os.environ.get("username")
password = os.environ.get("password")
number = os.environ.get("number")
location = os.environ.get("location")
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

# Now you can use the access_token for subsequent API requests
# For example, you can fetch data from a collection
collection_url = base_url + '/items/samples'
headers = {'Authorization': f'Bearer {access_token}'}
response = session.get(collection_url, headers=headers)
collection_data = response.json()['data']
print(collection_data)
# Process the collection data as needed
