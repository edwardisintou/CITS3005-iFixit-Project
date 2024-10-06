from owlready2 import *

# Load the ontology
ontology = get_ontology("ontology/phone_knowledge_graph.owl").load()

# Access classes and properties
Phone = ontology.Phone
Procedure = ontology.Procedure
Step = ontology.Step
Tool = ontology.Tool
has_step = ontology.has_step
uses_tool = ontology.uses_tool

# Query 1: Find all procedures with more than 6 steps
def find_procedures_with_more_than_6_steps():
    procedures = []
    for procedure in Procedure.instances():
        if len(procedure.has_step) > 6:
            procedures.append(procedure)
    return procedures

# Query 2: Find all items (phones) that have more than 10 procedures written for them
def find_items_with_more_than_10_procedures():
    items = []
    for phone in Phone.instances():
        procedures = set()
        for part in phone.has_part:
            procedures.update(part.has_procedure)  # Collect all procedures linked to this part
        if len(procedures) > 10:
            items.append(phone)
    return items

# Query 3: Find all procedures that include a tool that is never mentioned in the procedure steps
def find_procedures_with_unused_tools():
    procedures_with_unused_tools = []
    for procedure in Procedure.instances():
        tools_used_in_steps = set()
        for step in procedure.has_step:
            # Collect tools mentioned in the step's text (assuming there is a text attribute)
            step_text = getattr(step, 'text', '').lower()
            for tool in Tool.instances():
                if tool.name.lower() in step_text:
                    tools_used_in_steps.add(tool)
        
        # Check if there are tools in `uses_tool` that are not mentioned in the steps
        unused_tools = set(procedure.uses_tool) - tools_used_in_steps
        if unused_tools:
            procedures_with_unused_tools.append((procedure, unused_tools))
    return procedures_with_unused_tools

# Query 4: Flag potential hazards in the procedure by identifying steps with words like "careful" and "dangerous"
def flag_potential_hazards():
    hazardous_procedures = []
    for procedure in Procedure.instances():
        hazardous_steps = []
        for step in procedure.has_step:
            step_text = getattr(step, 'text', '').lower()
            if 'careful' in step_text or 'dangerous' in step_text:
                hazardous_steps.append(step)
        if hazardous_steps:
            hazardous_procedures.append((procedure, hazardous_steps))
    return hazardous_procedures

# Run the queries and print results
# Query 1
# procedures_with_more_than_6_steps = find_procedures_with_more_than_6_steps()
# print(f"Procedures with more than 6 steps: {[p.name for p in procedures_with_more_than_6_steps]}")

# Query 2
# items_with_more_than_10_procedures = find_items_with_more_than_10_procedures()
# print(f"Items with more than 10 procedures: {[item.name for item in items_with_more_than_10_procedures]}")

# # Query 3
procedures_with_unused_tools = find_procedures_with_unused_tools()
print("Procedures with unused tools:")
for procedure, unused_tools in procedures_with_unused_tools:
    print(f"- {procedure.name}: Unused tools - {[tool.name for tool in unused_tools]}")

# # Query 4
# hazardous_procedures = flag_potential_hazards()
# print("Procedures with hazardous steps:")
# for procedure, hazardous_steps in hazardous_procedures:
#     print(f"- {procedure.name}: Hazardous steps - {[step.name for step in hazardous_steps]}")
