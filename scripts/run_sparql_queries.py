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

# query1_results = g.query(query1)
# for result in query1_results:
#     procedure = str(result[0]).split('#')[-1]
#     print(format_result(procedure))


# Query 2: Find all items that have more than 10 procedures written for them;
# Result prints nothing because there is no such item
query2 = """
SELECT ?item (COUNT(?procedure) AS ?procedureCount)
WHERE {
  ?item a <http://example.org/phone_knowledge_graph.owl#Item> ;
        <http://example.org/phone_knowledge_graph.owl#has_procedure> ?procedure .
}
GROUP BY ?item
HAVING (COUNT(?procedure) > 10)
"""

query2_results = g.query(query2)
for result in query2_results:
    item = str(result[0]).split('#')[-1]
    formatted_name = format_result(item)
    print(formatted_name, "has", result[1], "procedures")
