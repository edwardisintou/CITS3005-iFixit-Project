import json
import hashlib
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
mentioned_tools = ontology.mentioned_tools
num_steps = ontology.num_steps

# Function to sanitize names for use as ontology individuals
def sanitize_name(name):
    sanitized_name = name.strip().replace(" ", "_").replace("-", "_").replace("/", "_").replace(":", "").replace("#", "")
    sanitized_name = ''.join(c for c in sanitized_name if c.isalnum() or c in ['_', '-'])

    # If the name is too long, hash it
    if len(sanitized_name) > 100:
        return hashlib.sha1(sanitized_name.encode()).hexdigest()
    
    return sanitized_name

# Dictionary to store procedure instances, their steps, and associated items/parts
procedure_instances = {}

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
            procedure_instance = Procedure(sanitize_name(phone_data["Title"]))
            part_instance.has_procedure.append(procedure_instance)

            # Store the procedure and the part it belongs to
            procedure_instances[procedure_instance] = (part_instance, [])
        else:
            # If "Subject" is empty or matches the item, create a procedure for the entire item
            procedure_instance = Procedure(sanitize_name(phone_data["Title"]))
            item_instance.has_procedure.append(procedure_instance)

            # Store the procedure and the item it belongs to
            procedure_instances[procedure_instance] = (item_instance, [])
        
        # Create instances of Tools using "Toolbox" "Name"
        tools = []
        for tool_data in phone_data.get("Toolbox", []):
            tool_name = tool_data["Name"]
            tool_instance = Tool(sanitize_name(tool_name))
            tools.append(tool_instance)
        
        # Link tools to the procedure
        tools = list(set(tools))
        if tools:
            procedure_instance.uses_tool = tools
        
        # Create instances of Steps and track tools mentioned in steps
        steps = []
        step_mentioned_tools = set()
        for step_data in phone_data.get("Steps", []):
            # Generate a step identifier based on the step text
            step_text_content = step_data.get("Text_raw", "").strip()
            step_instance = Step(sanitize_name(step_text_content))
            steps.append(step_instance)
            
            # Create Image instances and link them to the step
            images = [Image(sanitize_name(img.split('/')[-1])) for img in step_data.get("Images", [])]
            step_instance.has_image = images
            
            # Add the step text to the step instance
            step_instance.step_text = step_text_content
            
            # Check for tools mentioned in the step and add them to the procedure's toolbox if missing
            step_tools = step_data.get("Tools_extracted", [])
            for tool_name in step_tools:
                if tool_name and tool_name != "NA":
                    tool_instance = Tool(sanitize_name(tool_name))

                    # Add to the mentioned tools if not already included
                    if tool_instance not in step_mentioned_tools:
                        step_instance.mentioned_tools.append(tool_name)
                        step_mentioned_tools.add(tool_instance)

                    # Add to the procedure's toolbox if not already included
                    if tool_instance not in procedure_instance.uses_tool:
                        procedure_instance.uses_tool.append(tool_instance)

        # Link steps to the procedure
        steps = list(set(steps))
        if steps:
            procedure_instance.has_step = steps
        
        # Compare tools in procedure to tools mentioned in steps
        unmentioned_tools = set(procedure_instance.uses_tool) - step_mentioned_tools

        # Update the steps list in the dictionary
        procedure_instances[procedure_instance] = (procedure_instances[procedure_instance][0], steps)

# Infer sub-procedure relationships by comparing steps of each procedure
for proc1, (item1, steps1) in procedure_instances.items():
    for proc2, (item2, steps2) in procedure_instances.items():     
        steps1_texts = {step.step_text for step in steps1}
        steps2_texts = {step.step_text for step in steps2}
        
        # Ensure that proc1 is a subset of proc2 and that proc1 and proc2 are for the same item or its parts
        if proc1 != proc2 and steps1_texts.issubset(steps2_texts):
            if item1 == item2 or item1 in item2.has_part:
                # Avoid adding duplicate sub-procedures
                if proc1 not in proc2.has_sub_procedure:
                    proc2.has_sub_procedure.append(proc1)
            elif item1 == item2 or item2 in item1.has_part:
                # Ensure proc2 is also added as a sub-procedure of proc1 if applicable
                if proc2 not in proc1.has_sub_procedure:
                    proc1.has_sub_procedure.append(proc2)

# Save the populated ontology
ontology.save(file="ontology/phone_knowledge_graph.owl")
