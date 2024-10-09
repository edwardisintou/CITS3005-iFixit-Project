import json

with open('data/Phone.json') as f:
    steps1 = []
    steps2 = []

    for line in f:
        phone_data = json.loads(line.strip())
        # if phone_data['Title'] == 'iPhone 3G Battery Replacement':
        if phone_data['Title'] == 'iPhone 4 Rear Panel Replacement':
            for step in phone_data['Steps']:
                steps1.append(step['Text_raw'])

        elif phone_data['Title'] == 'Repairing iPhone 4 LCD Backlight Dim spot issue':
            for step in phone_data['Steps']:
                steps2.append(step['Text_raw'])

    for line in steps2:
        if line in steps1:
            # print(line)
            pass
        else:
            print("None")
    
# from owlready2 import *
# ontology = get_ontology("http://example.org/phone_ontology.owl")

# for procedure in ontology.Procedure.instances():
#     # Placeholder logic to identify sub-procedures
#     if "Replacement" in procedure.name:
#         print(procedure.name)
#         break


