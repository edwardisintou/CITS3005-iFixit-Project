import json
from owlready2 import *

# Load the ontology
ontology = get_ontology("ontology/phone_ontology.owl").load()

# Access classes and properties
Phone = ontology.Phone
Part = ontology.Part
Battery = ontology.Battery
Screen = ontology.Screen
AntennaCover = ontology.AntennaCover
SIMCardTray = ontology.SIMCardTray
HeadphoneJack = ontology.HeadphoneJack
Procedure = ontology.Procedure
Tool = ontology.Tool
OpeningTool = ontology.OpeningTool
Screwdriver = ontology.Screwdriver
Spudger = ontology.Spudger
SimCardEjectTool = ontology.SimCardEjectTool
Step = ontology.Step
Image = ontology.Image

is_part_of = ontology.is_part_of
has_part = ontology.has_part
uses_tool = ontology.uses_tool
has_step = ontology.has_step
has_image = ontology.has_image
has_sub_procedure = ontology.has_sub_procedure

# Function to sanitize names for use as ontology individuals
def sanitize_name(name):
    return name.strip().replace(" ", "_").replace("-", "_").replace("/", "_")

# Helper function to determine tool subclass
def get_tool_subclass(tool_name):
    tool_name_lower = tool_name.lower()
    if "opening tool" in tool_name_lower:
        return OpeningTool
    elif "screwdriver" in tool_name_lower:
        return Screwdriver
    elif "spudger" in tool_name_lower:
        return Spudger
    elif "sim card eject tool" in tool_name_lower:
        return SimCardEjectTool
    else:
        return Tool  # Default to the generic Tool class

# Helper function to determine part subclass from tool name
def get_part_subclass(tool_name):
    tool_name_lower = tool_name.lower()
    if "battery" in tool_name_lower:
        return Battery
    elif "screen" in tool_name_lower:
        return Screen
    elif "antenna cover" in tool_name_lower:
        return AntennaCover
    elif "sim card tray" in tool_name_lower:
        return SIMCardTray
    elif "headphone jack" in tool_name_lower:
        return HeadphoneJack
    else:
        return Part  # Default to the generic Part class

# Load and parse each line of the JSON file
with open('data/Phone.json') as f:
    for line in f:
        phone_data = json.loads(line.strip())
        
        # Create instances of Phone and Procedure
        phone_instance = Phone(sanitize_name(phone_data["Title"]))
        procedure_instance = Procedure(sanitize_name(phone_data["Title"]) + "_Procedure")
        
        # Link the procedure to the phone as a part of it
        phone_instance.has_part = [procedure_instance]
        
        # Create instances of Tools and Parts
        tools = []
        parts = []
        for tool_data in phone_data.get("Toolbox", []):
            tool_name = tool_data["Name"]
            url = tool_data.get("Url", "")
            
            # Check if url is not None and if it contains '/Parts/' to identify it as a part
        if url and '/Parts/' in url:
            # Create an instance of a part
            part_class = get_part_subclass(tool_name)
            part_instance = part_class(sanitize_name(tool_name))
            parts.append(part_instance)
        else:
            # Create an instance of a tool
            tool_class = get_tool_subclass(tool_name)
            tool_instance = tool_class(sanitize_name(tool_name))
            tools.append(tool_instance)
        
        # Link tools and parts to the procedure and phone
        procedure_instance.uses_tool = tools
        if parts:
            phone_instance.has_part.extend(parts)
        
        # Create instances of Steps
        steps = []
        for step_data in phone_data.get("Steps", []):
            # Create a Step instance
            step_instance = Step(f"Step_{step_data['Order']}")
            steps.append(step_instance)
            
            # Create Image instances and link them to the step
            images = [Image(sanitize_name(img.split('/')[-1])) for img in step_data.get("Images", [])]
            step_instance.has_image = images
        
        # Link steps to the procedure
        procedure_instance.has_step = steps

# After creating instances for phones, tools, parts, steps, etc., link sub-procedures
for procedure in ontology.Procedure.instances():
    # Placeholder logic to identify sub-procedures
    if "Replacement" in procedure.name:
        # Find or create another procedure that might be a sub-procedure
        sub_procedure_name = procedure.name.replace("Replacement", "SubProcedure")
        sub_procedure = ontology.Procedure(sanitize_name(sub_procedure_name))
        
        # Link the sub-procedure to the current procedure
        procedure.has_sub_procedure = [sub_procedure]

# Save the populated ontology
ontology.save(file="ontology/phone_knowledge_graph.owl")

