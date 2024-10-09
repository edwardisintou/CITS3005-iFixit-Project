import json

with open('data/Phone.json') as f:
    for line in f:
        phone_data = json.loads(line.strip())
        if phone_data['Title'] == 'Sony Xperia XZ Premium Battery Replacement':
            for step in phone_data['Steps']:
                print(step['Text_raw'])
    
# from owlready2 import *
# ontology = get_ontology("http://example.org/phone_ontology.owl")

# for procedure in ontology.Procedure.instances():
#     # Placeholder logic to identify sub-procedures
#     if "Replacement" in procedure.name:
#         print(procedure.name)
#         break

