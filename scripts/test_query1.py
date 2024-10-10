import json

with open('data/Phone.json') as f:
    for line in f:
        phone_data = json.loads(line.strip())
        if phone_data['Title'] == 'Motorola RAZR Maxx HD Front-Facing Camera Replacement':
            for step_data in phone_data.get("Steps", []):
                print(step_data['Order'])