import json

with open('data/Phone.json') as f:
    for line in f:
        phone_data = json.loads(line.strip())
        if phone_data['Title'] == 'iPhone 4 Rear Panel Replacement':
            for tool_data in phone_data.get("Toolbox", []):
                tool_name = tool_data["Name"]
                print(tool_name)
