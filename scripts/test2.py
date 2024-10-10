import json

with open('data/Phone.json') as f:
    for line in f:
        phone_data = json.loads(line.strip())
        if phone_data['Title'] == 'Blackberry DTek 60 Battery Replacement':
            for step_data in phone_data.get("Steps", []):
                step_tools = step_data.get("Tools_extracted", [])
                for tool_name in step_tools:
                    if tool_name and tool_name != "NA":
                        print(tool_name)


# phone_ontology.iPhone_3G_Display_Replacement is a sub-procedure of phone_ontology.iPhone_3GS_Display_Replacement
# phone_ontology.BlackBerry_7130e_Keypad_Replacement is a sub-procedure of phone_ontology.BlackBerry_7130e_Disassembly