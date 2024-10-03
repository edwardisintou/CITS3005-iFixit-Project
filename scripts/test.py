import json

with open('data/Phone.json') as f:
    for line in f:
        phone_data = json.loads(line.strip())
        print(phone_data['Toolbox'][0]['Url'])
        break
    