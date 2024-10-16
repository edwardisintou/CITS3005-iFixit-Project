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
    SELECT DISTINCT ?procedure (COUNT(?step) AS ?stepCount)
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
#     step_count = result[1]  # This will be the count of steps
#     print(f"Procedure {format_result(procedure)} has {step_count} steps")


# Query 2: Find all items that have more than 10 procedures written for them;
query2 = """
SELECT DISTINCT ?item (COUNT(?procedure) AS ?procedureCount)
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

# Result prints nothing because there is no such item
# This can be tested by printing items with less procedures (2 for example),
# which results in the item 'iphone 4S' having the most procedures of 6


# Query 3: Find all procedures that include a tool that is never mentioned in the procedure steps
query3 = """
SELECT DISTINCT ?procedure ?tool
WHERE {
  ?procedure a <http://example.org/phone_knowledge_graph.owl#Procedure> ;
             <http://example.org/phone_knowledge_graph.owl#unmentioned_tools> ?tool .
}
"""

# query_results3 = g.query(query3)
# for result in query_results3:
#     procedure = str(result[0]).split('#')[-1]
#     tool = str(result[1]).split('#')[-1]
    
#     formatted_procedure = format_result(procedure)
#     formatted_tool = format_result(tool)
    
#     print(f"Procedure {formatted_procedure} has Tool {formatted_tool} that is never mentioned")


# Query 4: Flag potential hazards in the procedure by identifying steps with works like "careful" and "dangerous"
query4 = """
SELECT DISTINCT ?procedure ?step ?stepText
WHERE {
  ?procedure a <http://example.org/phone_knowledge_graph.owl#Procedure> ;
             <http://example.org/phone_knowledge_graph.owl#has_step> ?step .
  
  ?step <http://example.org/phone_knowledge_graph.owl#step_text> ?stepText .
  
  FILTER(CONTAINS(LCASE(?stepText), "careful") || CONTAINS(LCASE(?stepText), "dangerous"))
}
"""

# query4_results = g.query(query4)
# for result in query4_results:
#     procedure = str(result[0]).split('#')[-1]
#     step = result[2]
    
#     print(f"Procedure: {format_result(procedure)}")
#     print(f"Step: {step}")
#     print("----")
