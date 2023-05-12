import requests
import json
import pandas as pd

# Credentials and endpoints
credentials = {
    'committee_1': {'api_key': 'your_api_key_1', 'committee_id': 'committee_id_1'},
    'committee_2': {'api_key': 'your_api_key_2', 'committee_id': 'committee_id_2'},
    'committee_3': {'api_key': 'your_api_key_3', 'committee_id': 'committee_id_3'}
}

api_base_url = 'https://api.securevan.com/v4'
optout_endpoint = '/people/optouts'

# Read in the opt-out data CSV file
# File must contain VANID, Committee, & OptOut Date columns
# Can BQ table query be used instead of a csv?
optout_data = pd.read_csv('optout_data.csv')

# Loop through the opt-out data and update the appropriate voter records
for _, row in optout_data.iterrows():
    # Get the API key and committee ID for this opt-out record
    committee = row['committee']
    api_key = credentials[committee]['api_key']
    committee_id = credentials[committee]['committee_id']
    
    # Construct the API endpoint URL
    endpoint_url = api_base_url + f'/committees/{committee_id}' + optout_endpoint
    
    # Construct the payload for the API call
    payload = {
        'vanId': int(row['vanid']),
        'date': row['optout_date'],
        'method': 'VAN_OPTOUT',
        'optOutType': 'DO_NOT_TEXT'
    }
    
    # Make the API call to update the voter record
    response = requests.post(
        endpoint_url,
        headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'},
        data=json.dumps(payload)
    )
    
    # Check the response and print any errors
    if response.status_code != 200:
        print(f"Error updating voter record with VAN ID {row['vanid']} in committee {committee}: {response.content}")
