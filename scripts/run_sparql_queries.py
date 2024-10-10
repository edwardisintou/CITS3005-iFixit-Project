from rdflib import Graph

# Load the RDFLib graph
g = Graph()
g.parse("ontology/phone_knowledge_graph.owl")

# Function to format the result by replacing underscores with spaces
def format_result(name):
    return name.replace('_', ' ')

# SPARQL queries on the graph
# Query 1: Find all procedures with more than 6 steps
query1 = """
    SELECT DISTINCT ?procedure
    WHERE {
      ?procedure rdf:type <http://example.org/phone_knowledge_graph.owl#Procedure> .
      ?procedure <http://example.org/phone_knowledge_graph.owl#has_step> ?step .
    }
    GROUP BY ?procedure
    HAVING (COUNT(?step) > 6)
"""
query1_results = g.query(query1)
for result in query1_results:
    procedure = str(result[0]).split('#')[-1]
    print(format_result(procedure))
