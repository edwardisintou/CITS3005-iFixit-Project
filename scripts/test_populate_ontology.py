from owlready2 import *

# Load the populated ontology
ontology = get_ontology("ontology/phone_knowledge_graph.owl").load()

# Reason over the ontology to apply restrictions and infer relationships
with ontology:
    sync_reasoner()

# Check instances of the Phone class
print("Instances of Phone:")
for phone in ontology.Phone.instances()[:5]:
    print(f"- {phone.name}")
    print(f"  Parts: {[part.name for part in phone.has_part]}")

# Check instances of the Procedure class
print("\nInstances of Procedure:")
for procedure in ontology.Procedure.instances()[:5]:
    print(f"- {procedure.name}")
    print(f"  Tools: {[tool.name for tool in procedure.uses_tool]}")
    print(f"  Steps: {[step.name for step in procedure.has_step]}")

# Check if the restrictions are working
print("\nTesting restrictions:")

# Check if each Phone has at least one part (restriction on Phone class)
for phone in ontology.Phone.instances()[:5]:
    if ontology.has_part in phone.get_properties():
        print(f"{phone.name} has parts: {[part.name for part in phone.has_part]}")
    else:
        print(f"{phone.name} does not satisfy the restriction: 'has_part.some(Part)'")

# Check if each Procedure uses at least one tool and has at least one step (restriction on Procedure class)
for procedure in ontology.Procedure.instances()[:5]:
    if ontology.uses_tool in procedure.get_properties() and ontology.has_step in procedure.get_properties():
        print(f"{procedure.name} satisfies the restriction: 'uses_tool.some(Tool) & has_step.some(Step)'")
    else:
        print(f"{procedure.name} does not satisfy the restriction.")

# Check if each Step has at least one image (restriction on Step class)
for step in ontology.Step.instances()[:5]:
    if ontology.has_image in step.get_properties():
        print(f"{step.name} has images: {[img.name for img in step.has_image]}")
    else:
        print(f"{step.name} does not satisfy the restriction: 'has_image.some(Image)'")
