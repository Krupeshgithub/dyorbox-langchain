import requests
import json

def fetch_and_save_data():
    url = 'https://dyorbox.io/api/projects?from=0&rows=100'
    headers = {
        'Accept': 'application/json, text/plain, /',
        'Connection': 'keep-alive',
        'If-None-Match': 'W/"24fb-XTuxcmL1X2azAlVteDJ8XwJHdjM"',
        'Referer': 'https://dyorbox.io/projects',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-GPC': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'accept-language': 'en-GB,en;q=0.5',
        'authtoken': '6ef3c9ab-c285-478a-be42-524cf5517f66',
        'platform': 'web',
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # Successful response, save to response.json
        with open('documents/response.json', 'w') as file:
            json.dump(response.json().get("data", {}), file, indent=4)
        print("Dataset loaded to dataset.json")
    else:
        # Handle other status codes if needed
        print(f"Failed to load dataset. Status code: {response.status_code}")

# Call the function to execute the request and save the data
fetch_and_save_data()
