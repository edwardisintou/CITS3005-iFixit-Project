import json
from owlready2 import *

# Load the ontology
ontology = get_ontology("ontology/phone_ontology.owl").load()

# Access classes from the loaded ontology
Phone = ontology.Phone
Part = ontology.Part
Tool = ontology.Tool
Procedure = ontology.Procedure
Step = ontology.Step

with ontology:
    # Open the JSON file and read each line as a separate JSON object
    with open('data/Phone.json') as f:
        for line in f:
            phone_data = json.loads(line.strip())
            
            # Create instances for the procedure
            procedure_instance = Procedure(phone_data["Title"])
            
            # Create tool instances
            tools = []
            for tool_data in phone_data["Toolbox"]:
                tool_instance = Tool(tool_data["Name"])
                tools.append(tool_instance)
            
            # Link tools to the procedure
            procedure_instance.uses_tool = tools
            
            # Create step instances
            for step_data in phone_data["Steps"]:
                step_instance = Step(f"Step_{step_data['Order']}")
                step_instance.text = step_data["Text_raw"]
                procedure_instance.has_step.append(step_instance)

# Save the populated ontology
ontology.save(file="ontology/phone_knowledge_graph.owl")
