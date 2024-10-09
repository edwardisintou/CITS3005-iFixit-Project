import json

with open('data/Phone.json') as f:
    for line in f:
        phone_data = json.loads(line.strip())
        # ancestors = phone_data.get("Ancestors", [])
        # print(ancestors)
        print(phone_data.keys())
        print(phone_data['Steps'][0]['Tools_extracted'])
        # print(phone_data['Steps'][0]['Images'])
        break
    
# from owlready2 import *
# ontology = get_ontology("http://example.org/phone_ontology.owl")

# for procedure in ontology.Procedure.instances():
#     # Placeholder logic to identify sub-procedures
#     if "Replacement" in procedure.name:
#         print(procedure.name)
#         break

