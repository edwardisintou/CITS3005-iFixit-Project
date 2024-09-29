from owlready2 import *

ontology = get_ontology("http://example.org/phone_ontology.owl")

with ontology:
    # Define classes
    class Phone(Thing): pass
    class Part(Thing): pass
    class Tool(Thing): pass
    class Procedure(Thing): pass
    class Step(Thing): pass
    class Image(Thing): pass

    # Define properties
    class has_part(Phone >> Part): pass
    class uses_tool(Procedure >> Tool): pass
    class has_step(Procedure >> Step): pass
    class has_image(Step >> Image): pass

ontology.save(file="ontology/phone_ontology.owl")
