import json

with open('data/Phone.json') as f:
    for line in f:
        phone_data = json.loads(line.strip())
        if phone_data['Title'] == 'Panasonic KX TG6021M Front Speaker Replacement':
            for step_data in phone_data.get("Steps", []):
                print(step_data['Order'])