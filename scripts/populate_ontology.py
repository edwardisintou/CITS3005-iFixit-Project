import json
from owlready2 import *

# Load the ontology
ontology = get_ontology("ontology/phone_ontology.owl").load()

# Access classes
Phone = ontology.Phone
Procedure = ontology.Procedure
Part = ontology.Part
Step = ontology.Step
Image = ontology.Image
Tool = ontology.Tool

# Access subclasses of Tool
OpeningTool = ontology.OpeningTool
Screwdriver = ontology.Screwdriver
Spudger = ontology.Spudger
Tweezers = ontology.Tweezers

# Access subclasses of Part
OpeningToolPart = ontology.OpeningToolPart
ScrewdriverPart = ontology.ScrewdriverPart

# Access properties
is_part_of = ontology.is_part_of
has_part = ontology.has_part
has_procedure = ontology.has_procedure
uses_tool = ontology.uses_tool
has_step = ontology.has_step
has_image = ontology.has_image
has_sub_procedure = ontology.has_sub_procedure

# Function to sanitize names for use as ontology individuals
def sanitize_name(name):
    # Remove or replace illegal characters
    sanitized_name = name.strip().replace(" ", "_").replace("-", "_").replace("/", "_").replace(":", "").replace("#", "")
    # Handle URLs by extracting a meaningful part
    if 'http' in sanitized_name:
        sanitized_name = sanitized_name.split('_')[-1]  # Take the last segment after underscores
    return sanitized_name

# Helper function to determine tool subclass
def get_tool_subclass(tool_name):
    tool_name_lower = tool_name.lower()
    if "opening tool" in tool_name_lower:
        return OpeningTool
    elif "screwdriver" in tool_name_lower:
        return Screwdriver
    elif "spudger" in tool_name_lower:
        return Spudger
    elif "tweezers" in tool_name_lower:
        return Tweezers
    else:
        return Tool  # Default to the generic Tool class

# Helper function to determine part subclass from tool name
def get_part_subclass(tool_name):
    tool_name_lower = tool_name.lower()
    if "opening tool" in tool_name_lower:
        return OpeningToolPart
    elif "screwdriver" in tool_name_lower:
        return ScrewdriverPart
    else:
        return Part  # Default to the generic Part class

# Load and parse each line of the JSON file
with open('data/Phone.json') as f:
    for line in f:
        phone_data = json.loads(line.strip())
        
        # Create instances of Phone
        phone_instance = Phone(sanitize_name(phone_data["Title"]))
        
        # Create instances of Parts and link to the phone
        parts = []
        tools = []
        for tool_data in phone_data.get("Toolbox", []):
            tool_name = tool_data["Name"]
            url = tool_data.get("Url", "")
            
            if url and '/Parts/' in url:
                # Create an instance of the Part and link to the phone
                part_class = get_part_subclass(tool_name)
                part_instance = part_class(sanitize_name(tool_name))
                parts.append(part_instance)
                phone_instance.has_part.append(part_instance)
                
                # Create a Procedure instance for this part
                procedure_instance = Procedure(sanitize_name(phone_data["Title"]) + "_Procedure")
                
                # Link the Procedure to the Part
                part_instance.has_procedure = [procedure_instance]

                # Link the Procedure to the Phone as part of the overall process
                phone_instance.has_part.append(procedure_instance)

            else:
                # Treat as a tool
                tool_class = get_tool_subclass(tool_name)
                tool_instance = tool_class(sanitize_name(tool_name))
                tools.append(tool_instance)

        # Create the Procedure instance for the phone (if not already created)
        if not 'procedure_instance' in locals():
            procedure_instance = Procedure(sanitize_name(phone_data["Title"]) + "_Procedure")
            phone_instance.has_part.append(procedure_instance)
        
        # Link tools to the procedure (if there are any)
        if tools:
            procedure_instance.uses_tool = tools
        
        # Create instances of Steps
        steps = []
        for step_data in phone_data.get("Steps", []):
            step_instance = Step(f"Step_{step_data['Order']}")
            steps.append(step_instance)
            
            # Create Image instances and link them to the step
            images = [Image(sanitize_name(img.split('/')[-1])) for img in step_data.get("Images", [])]
            step_instance.has_image = images
        
        # Link steps to the procedure
        if steps:
            procedure_instance.has_step = steps

# After creating instances for phones, tools, parts, steps, etc., link sub-procedures
# for procedure in ontology.Procedure.instances():
#     if "Replacement" in procedure.name:
#         sub_procedure_name = procedure.name.replace("Replacement", "SubProcedure")
        
#         # Find an existing sub-procedure or skip creation if not needed
#         existing_sub_procedures = [proc for proc in ontology.Procedure.instances() if proc.name == sanitize_name(sub_procedure_name)]
        
#         if existing_sub_procedures:
#             # Link the existing sub-procedure
#             procedure.has_sub_procedure = [existing_sub_procedures[0]]

for procedure_instance in ontology.Procedure.instances():
    print(f"Procedure: {procedure_instance.name}, Steps: {[step.name for step in procedure_instance.has_step]}")

# Save the populated ontology
ontology.save(file="ontology/phone_knowledge_graph.owl")
