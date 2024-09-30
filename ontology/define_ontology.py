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

    # Define properties with more specific domains and ranges
    class has_part(ObjectProperty):
        domain = [Phone]
        range = [Part]

    class uses_tool(ObjectProperty):
        domain = [Procedure]
        range = [Tool]

    class has_step(ObjectProperty):
        domain = [Procedure]
        range = [Step]

    class has_image(ObjectProperty):
        domain = [Step]
        range = [Image]

    # Add restrictions directly to the primary classes
    Phone.equivalent_to = [has_part.some(Part)]
    Procedure.equivalent_to = [uses_tool.some(Tool) & has_step.some(Step)]
    Step.equivalent_to = [has_image.some(Image)]

# Save the ontology
ontology.save(file="ontology/phone_ontology.owl")
