import json

with open('data/Phone.json') as f:
    for line in f:
        phone_data = json.loads(line.strip())
        print(phone_data['Steps'][1]['Text_raw'])
        break

phone_ontology.iPhone_3G_Display_Replacement is a sub-procedure of phone_ontology.iPhone_3GS_Display_Replacement