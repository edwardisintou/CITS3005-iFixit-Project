from owlready2 import *

ontology = get_ontology("http://example.org/phone_knowledge_graph.owl")

with ontology:
    # Define classes
    class Item(Thing): pass  # General item, such as a phone
    class Part(Item): pass  # Parts of an item; subclass of Item to inherit properties
    class Procedure(Thing): pass  # Repair or replacement procedures
    class Tool(Thing): pass  # Tools used in procedures
    class Step(Thing): pass  # Individual steps in a procedure
    class Image(Thing): pass  # Images associated with steps

    # Object properties
    class has_part(ObjectProperty):
        domain = [Item]
        range = [Part]
        is_transitive = True

    class is_part_of(ObjectProperty):
        domain = [Part]
        range = [Item]
        inverse_property = has_part

    class has_procedure(ObjectProperty):
        domain = [Item, Part]  # Allow both Items and Parts to have procedures
        range = [Procedure]

    class is_procedure_for(ObjectProperty):
        domain = [Procedure]
        range = [Item, Part]
        inverse_property = has_procedure

    class uses_tool(ObjectProperty):
        domain = [Procedure]
        range = [Tool]

    class is_used_by(ObjectProperty):
        domain = [Tool]
        range = [Procedure]
        inverse_property = uses_tool

    class has_step(ObjectProperty):
        domain = [Procedure]
        range = [Step]

    class is_step_of(ObjectProperty):
        domain = [Step]
        range = [Procedure]
        inverse_property = has_step

    class has_image(ObjectProperty):
        domain = [Step]
        range = [Image]

    class is_image_of(ObjectProperty):
        domain = [Image]
        range = [Step]
        inverse_property = has_image

    class has_sub_procedure(ObjectProperty):
        domain = [Procedure]
        range = [Procedure]
        is_transitive = True

    class is_sub_procedure_of(ObjectProperty):
        domain = [Procedure]
        range = [Procedure]
        inverse_property = has_sub_procedure

    class unmentioned_tools(ObjectProperty):
        domain = [Procedure]
        range = [Tool]

    # Data properties
    class step_text(DataProperty, FunctionalProperty):  # Store the text description of each step
        domain = [Step]
        range = [str]

    class mentioned_tools(DataProperty):  # Tools mentioned in the step's text
        domain = [Step]
        range = [str]

    # Add restrictions
    Item.equivalent_to = [has_part.some(Part) | has_procedure.some(Procedure)] # An Item can have parts or procedures
    Part.equivalent_to = [is_part_of.some(Item) | has_procedure.some(Procedure)]  # A Part can have procedures or be part of an Item
    Procedure.equivalent_to = [uses_tool.some(Tool) & has_step.some(Step)]  # A Procedure uses tools and has steps
    Step.equivalent_to = [has_image.some(Image)]  # A Step has an associated image

# Save the ontology
ontology.save(file="ontology/phone_ontology.owl")
