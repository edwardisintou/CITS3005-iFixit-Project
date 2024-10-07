from owlready2 import *

ontology = get_ontology("http://example.org/phone_knowledge_graph.owl")

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
    class Tweezers(Tool): pass

    # Define subclasses of Part
    class OpeningToolPart(Part): pass
    class ScrewdriverPart(Part): pass

    # Define object properties
    class has_part(ObjectProperty):
        domain = [Phone]
        range = [Part]
        is_transitive = True

    class is_part_of(ObjectProperty):
        domain = [Part]
        range = [Phone]
        inverse_property = has_part

    class has_procedure(ObjectProperty):
        domain = [Part]
        range = [Procedure]

    class is_procedure_for(ObjectProperty):
        domain = [Procedure]
        range = [Part]
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

    # Add restrictions directly to the primary classes
    Phone.equivalent_to = [has_part.some(Part)]
    Part.equivalent_to = [has_procedure.some(Procedure)]
    Procedure.equivalent_to = [uses_tool.some(Tool) & has_step.some(Step) & has_sub_procedure.only(Procedure)]
    Step.equivalent_to = [has_image.some(Image)]

# Save the ontology
ontology.save(file="ontology/phone_ontology.owl")
