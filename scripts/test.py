# import json

# with open('data/Phone.json') as f:
#     for line in f:
#         phone_data = json.loads(line.strip())
#         print(phone_data.keys())
#         break
    
from owlready2 import *

# Load the populated ontology
ontology = get_ontology("ontology/phone_knowledge_graph.owl").load()

# Check all instances of the main classes
# print("Instances of Phone:")
# for phone in ontology.Phone.instances():
#     print(f"- {phone.name}")

# print("\nInstances of Part:")
# for part in ontology.Part.instances():
#     print(f"- {part.name}")

# print("\nInstances of Procedure:")
# for procedure in ontology.Procedure.instances():
#     print(f"- {procedure.name}")

# print("\nInstances of Tool:")
# for tool in ontology.Tool.instances():
#     print(f"- {tool.name}")

# print("\nInstances of Step:")
# for step in ontology.Step.instances():
#     print(f"- {step.name}")

# print("\nInstances of Image:")
# for image in ontology.Image.instances():
#     print(f"- {image.name}")

# Check relationships for Phones
# print("\nPhone and its parts:")
# for phone in ontology.Phone.instances():
#     print(f"{phone.name} has parts: {[part.name for part in phone.has_part]}")

# # Check relationships for Procedures
# print("\nProcedures and their tools:")
# for procedure in ontology.Procedure.instances():
#     print(f"{procedure.name} uses tools: {[tool.name for tool in procedure.uses_tool]}")

# print("\nProcedures and their steps:")
# for procedure in ontology.Procedure.instances():
#     print(f"{procedure.name} has steps: {[step.name for step in procedure.has_step]}")

# # Check relationships for Steps
# print("\nSteps and their images:")
# for step in ontology.Step.instances():
#     print(f"{step.name} has images: {[image.name for image in step.has_image]}")

# Run reasoning to infer relationships
with ontology:
    sync_reasoner()

# Check if constraints are enforced
# for phone in ontology.Phone.instances():
#     for part in phone.has_part:
#         print(f"{phone.name} has part: {part.name}")
#         # Check if part-of relationship is inferred correctly
#         print(f"Part {part.name} is part of: {[obj.name for obj in part.is_part_of]}")

# Check the subclass relationships for Procedures
for procedure in ontology.Procedure.instances():
    sub_procedures = procedure.has_sub_procedure
    if sub_procedures:
        print(f"{procedure.name} has sub-procedures: {[sub_proc.name for sub_proc in sub_procedures]}")


