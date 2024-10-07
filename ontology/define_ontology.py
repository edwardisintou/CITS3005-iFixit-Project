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

    # New property to aggregate part procedures under an item
    class has_part_procedure(ObjectProperty):
        domain = [Item]
        range = [Procedure]

    # Data properties
    class has_title(DataProperty):  # Store the title of the procedure
        domain = [Procedure]
        range = [str]

    class has_url(DataProperty):  # Store URLs for items, procedures, tools, etc.
        domain = [Thing]
        range = [str]

    class step_order(DataProperty):  # Store the order of steps
        domain = [Step]
        range = [int]

    class step_text(DataProperty):  # Store the text description of each step
        domain = [Step]
        range = [str]

    class mentioned_tools(DataProperty):  # Tools mentioned in the step's text
        domain = [Step]
        range = [str]

    class num_steps(DataProperty):  # Store the number of steps in a procedure
        domain = [Procedure]
        range = [int]

    # Add restrictions directly to the primary classes
    Item.equivalent_to = [has_part.some(Part) | has_procedure.some(Procedure) | has_part_procedure.some(Procedure)] # An Item can have parts or procedures
    Part.equivalent_to = [is_part_of.some(Item) | has_procedure.some(Procedure)]  # A Part can have procedures or be part of an Item
    Procedure.equivalent_to = [uses_tool.some(Tool) & has_step.some(Step)]  # A Procedure uses tools and has steps
    Step.equivalent_to = [has_image.some(Image)]  # A Step has an associated image

    # Rule: Aggregate part procedures to the item
    rule = Imp()
    rule.set_as_rule("""
        Item(?item), has_part(?item, ?part), has_procedure(?part, ?procedure) -> has_part_procedure(?item, ?procedure)
    """)

# Save the ontology
ontology.save(file="ontology/phone_ontology.owl")
