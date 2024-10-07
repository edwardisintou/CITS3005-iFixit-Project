import json
from owlready2 import *

# Load the ontology
ontology = get_ontology("ontology/phone_ontology.owl").load()

# Access classes
Item = ontology.Item
Procedure = ontology.Procedure
Part = ontology.Part
Step = ontology.Step
Image = ontology.Image
Tool = ontology.Tool

# Access properties
is_part_of = ontology.is_part_of
has_part = ontology.has_part
has_procedure = ontology.has_procedure
uses_tool = ontology.uses_tool
has_step = ontology.has_step
has_image = ontology.has_image
has_sub_procedure = ontology.has_sub_procedure
has_title = ontology.has_title
step_text = ontology.step_text
num_steps = ontology.num_steps

# Function to sanitize names for use as ontology individuals
def sanitize_name(name):
    sanitized_name = name.strip().replace(" ", "_").replace("-", "_").replace("/", "_").replace(":", "").replace("#", "")
    return sanitized_name

# Load and parse each line of the JSON file
with open('data/Phone.json') as f:
    for line in f:
        phone_data = json.loads(line.strip())
        
        # Create an Item instance
        item_name = sanitize_name(phone_data["Category"])
        item_instance = Item(item_name)
        
        # Determine how to handle the procedure based on the "Subject" field
        part_name = phone_data.get("Subject", "").strip()
        if part_name and part_name != phone_data["Category"]:
            # Create a Part instance and link to the item
            part_instance = Part(sanitize_name(part_name))
            item_instance.has_part.append(part_instance)

            # Create a procedure instance for this part
            procedure_instance = Procedure(sanitize_name(phone_data["Title"]) + "_Procedure")
            part_instance.has_procedure.append(procedure_instance)
        else:
            # If "Subject" is empty or matches the item, create a procedure for the entire item
            procedure_instance = Procedure(sanitize_name(phone_data["Title"]) + "_Procedure")
            item_instance.has_procedure.append(procedure_instance)
        
        # Create instances of Tools using "Toolbox" "Name"
        tools = []
        for tool_data in phone_data.get("Toolbox", []):
            tool_name = tool_data["Name"]
            tool_instance = Tool(sanitize_name(tool_name))
            tools.append(tool_instance)
        
        # Link tools to the procedure
        if tools:
            procedure_instance.uses_tool = tools
            # print(procedure_instance, procedure_instance.uses_tool)
        
        # Create instances of Steps
        steps = []
        for step_data in phone_data.get("Steps", []):
            step_instance = Step(f"{sanitize_name(phone_data['Title'])}_Step_{step_data['Order']}")
            steps.append(step_instance)
            
            # Create Image instances and link them to the step
            images = [Image(sanitize_name(img.split('/')[-1])) for img in step_data.get("Images", [])]
            step_instance.has_image = images
            
            # Add the step text to the step instance
            step_instance.step_text = step_data.get("Text_raw", "")
        
        # Link steps to the procedure
        if steps:
            procedure_instance.has_step = steps

        # # Debug: Print created instances
        # print(f"Created Item: {item_name}")
        # if part_name:
        #     print(f" - Part: {part_instance.name}")
        # print(f" - Procedure: {procedure_instance.name}")
        # for tool in tools:
        #     print(f" - Tool: {tool.name}")
        # for step in steps:
        #     print(f" - Step: {step.name} has image: {step.has_image}")


# Save the populated ontology
ontology.save(file="ontology/phone_knowledge_graph.owl")