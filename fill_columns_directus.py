# This script is a tool to manually alter the directus database for multiple columns, 
# please handle with care

import requests

# Define the Directus base URL

username = "username" #Change it with your directus username
password = "password" #Change it with your directus password
base_url = 'http://directus.dbgi.org' #Change it with your directus instance
collection = "Lab_Extracts" #Change it with the collection you want to fill
donnor_col = "lab_extract_id" #Change it with the donnor column
receiver_col = "field_sample_id" #Change it with the receiver column

# And don't forget to change the filling logic after "for item in data['data']:"

collection_prefix = "/items/"
collection_url = base_url + collection_prefix + collection

# Define the login endpoint URL
login_url = base_url + '/auth/login'
# Create a session object for making requests
try:
    session = requests.Session()
    # Send a POST request to the login endpoint
    response = session.post(login_url, json={'email': username, 'password': password})
    if response.status_code == 200:
        data = response.json()['data']
        access_token = data['access_token']

        # Fetch data from the Directus collection

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }

        # Fetch data from the Directus collection with maximum limit
        params = {
            'limit': -1  # Fetch the maximum allowed number of items
        }

        response = requests.get(collection_url, headers=headers, params=params)
        data = response.json()

        # Iterate through each row and update the desired column
        for item in data['data']:
            # Assuming 'source_column' contains the content you want to copy
            source_value = item[donnor_col]
            
            # Change logic from here...
            parts = source_value.split("_")
            
            up_value = parts[0] + "_" + parts[1]
            # Update 'target_column' with the value from 'source_column'
            item[receiver_col] = up_value

            # ...to here

            # Update the item in the collection
            item_id = item[donnor_col]
            update_url = collection_url + f'/{item_id}'
            update_response = requests.patch(update_url, headers=headers, json={receiver_col: up_value})

            if update_response.status_code == 200:
                print(f"Updated item {source_value} successfully!")
            else:
                print(f"Failed to update item {source_value}")

    else:
        print("Crontrol your credentials")

except:
    print("Make sure you are connected to the UNIFR network")