from owlready2 import *

# Load or create an ontology
ontology = get_ontology("http://example.org/phone_ontology.owl")

with ontology:
    # Define classes
    class Item(Thing): pass
    class Phone(Item): pass
    class Smartphone(Phone): pass

# Here, Smartphone is a subclass of Phone, and Phone is a subclass of Item
print(Smartphone.is_a)
# Output: [Phone]
print(Phone.is_a)
# Output: [Item]
