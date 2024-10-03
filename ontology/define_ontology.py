from owlready2 import *

ontology = get_ontology("http://example.org/phone_ontology.owl")

with ontology:
    # Define classes
    class Phone(Thing): pass
    class Part(Thing): pass
    class Procedure(Thing): pass
    class Tool(Thing): pass
    class Step(Thing): pass
    class Image(Thing): pass

    # Define subclasses of Tool
    class OpeningTool(Tool): pass
    class Spudger(Tool): pass
    class Screwdriver(Tool): pass
    class SimCardEjectTool(Tool): pass

    # Define subclasses of Part
    class AntennaCover(Part): pass
    class SIMCardTray(Part): pass
    class HeadphoneJack(Part): pass
    class Battery(Part): pass
    class Screen(Part): pass

    # Define properties with more specific domains and ranges
    class is_part_of(ObjectProperty):
        domain = [Part]
        range = [Thing]
        is_transitive = True

    class has_part(ObjectProperty):
        domain = [Phone]
        range = [Thing]
        inverse_property = is_part_of

    class uses_tool(ObjectProperty):
        domain = [Procedure]
        range = [Tool]

    class has_step(ObjectProperty):
        domain = [Procedure]
        range = [Step]

    class has_image(ObjectProperty):
        domain = [Step]
        range = [Image]

    class has_sub_procedure(ObjectProperty):
        domain = [Procedure]
        range = [Procedure]

    # Add restrictions directly to the primary classes
    Phone.equivalent_to = [has_part.some(Part)]
    Procedure.equivalent_to = [uses_tool.some(Tool) & has_step.some(Step) & has_sub_procedure.only(Procedure)]
    Step.equivalent_to = [has_image.some(Image)]

# Save the ontology
ontology.save(file="ontology/phone_ontology.owl")
