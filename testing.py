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
# Can BQ table query be referenced & used instead of a csv?
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
        
        
#### ----- using parsons ---- #####

import parsons
import os

# Set up NGP VAN credentials
NGP_VAN_API_KEY_1 = os.getenv('NGP_VAN_API_KEY_1')
NGP_VAN_API_KEY_2 = os.getenv('NGP_VAN_API_KEY_2')
NGP_VAN_API_KEY_3 = os.getenv('NGP_VAN_API_KEY_3')

# Set up the committees and their respective API keys
committees = {
    'committee_1': NGP_VAN_API_KEY_1,
    'committee_2': NGP_VAN_API_KEY_2,
    'committee_3': NGP_VAN_API_KEY_3
}

# Set up the file path to the CSV file
csv_file_path = '/path/to/optout_records.csv'

# Create a Parsons Table object from the CSV file
optout_table = parsons.Table.from_csv(csv_file_path)

# Loop through each committee and upload the optout records
for committee, api_key in committees.items():
    # Set up the NGP VAN client
    client = parsons.ngpvan.NGPVan(api_key)
    
    # Filter the optout table to the current committee
    filtered_table = optout_table.select_rows(lambda row: row['committee'] == committee)
    
    # Map the table fields to the NGP VAN fields
    field_map = {
        'vanid': 'VANID',
        'committee': 'CampaignID',
        'opt_out_date': 'DoNotTextDate',
        'do_not_text': 'DoNotText'
    }
    
    # Upload the optout records to NGP VAN
    client.upload(
        table=filtered_table,
        table_name='optout_records',
        field_map=field_map,
        allow_truncate=True
    )


# Example csv
vanid,committee,opt_out_date
12345,committee_1,2022-06-01
67890,committee_1,2022-06-02
23456,committee_2,2022-06-03
78901,committee_2,2022-06-04
34567,committee_3,2022-06-05
89012,committee_3,2022-06-06
