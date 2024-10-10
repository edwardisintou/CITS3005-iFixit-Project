from owlready2 import *
import rdflib

# Load the ontology
ontology = get_ontology("ontology/phone_knowledge_graph.owl").load()

# Convert OWL ontology to RDFLib graph
rdf_graph = ontology.world.as_rdflib_graph()

# Function to format result by removing underscores and capitalizing words
def format_result(name):
    # Replace underscores with spaces
    formatted_name = name.replace('_', ' ')
    return formatted_name

# SPARQL queries on the graph
# Query 1: Find all procedures with more than 6 steps
query1 = """
    SELECT ?procedure
    WHERE {
      ?procedure rdf:type <http://example.org/phone_knowledge_graph.owl#Procedure> .
      ?procedure <http://example.org/phone_knowledge_graph.owl#has_step> ?step .
    }
    GROUP BY ?procedure
    HAVING (COUNT(?step) > 6)
"""
query_results = rdf_graph.query(query1)
for result in query_results:
    procedure = str(result[0]).split('#')[-1]
    print(format_result(procedure))
