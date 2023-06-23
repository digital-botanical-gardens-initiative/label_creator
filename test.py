import requests
import os

#Variables of the first window (generate from scratch)
username = os.environ.get("VARIABLE_NAME")
print(username)
password = os.environ.get("VARIABLE_NAME")
print(password)
number = os.environ.get("VARIABLE_NAME")
print(number)
location = os.environ.get("VARIABLE_NAME")
print(location)
parambig1 = os.environ.get("VARIABLE_NAME")
print(parambig1)
paramsmall11 = os.environ.get("VARIABLE_NAME")
print(paramsmall11)
paramsmall21 = os.environ.get("VARIABLE_NAME")
print(paramsmall21)

#Variables of the second window (from existing)
number_ext = os.environ.get("VARIABLE_NAME")
print(number_ext)
number_inj = os.environ.get("VARIABLE_NAME")
print(number_inj)
parambig2 = os.environ.get("VARIABLE_NAME")
print(parambig2)
paramsmall12 = os.environ.get("VARIABLE_NAME")
print(paramsmall12)
paramsmall22 = os.environ.get("VARIABLE_NAME")
print(paramsmall22)
df = os.environ.get("VARIABLE_NAME")
print(df)




# Define the Directus base URL
base_url = 'http://directus.dbgi.org'

# Define the login endpoint URL
login_url = base_url + '/auth/login'

# Define the email and password for authentication
email = 'edouard.bruelhart@unifr.ch'
password = '861510Eb.98'

# Create a session object for making requests
session = requests.Session()

# Send a POST request to the login endpoint
response = session.post(login_url, json={'email': email, 'password': password})

# Check the response status
if response.status_code == 200:
    # Authentication successful
    data = response.json()['data']
    access_token = data['access_token']
    refresh_token = data['refresh_token']

    # Now you can use the access_token for subsequent API requests
    # For example, you can fetch data from a collection
    collection_url = base_url + '/items/samples'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = session.get(collection_url, headers=headers)
    if response.status_code == 200:
        # Successful response
        collection_data = response.json()['data']
        print(collection_data)
        # Process the collection data as needed
    else:
        # Handle error response
        print('Error:', response.status_code, response.text)
else:
    # Authentication failed
    print('Authentication failed:', response.status_code, response.text)
