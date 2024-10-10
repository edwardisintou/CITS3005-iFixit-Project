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
# query2 = """
# SELECT ?item (COUNT(?procedure) AS ?procedureCount)
# WHERE {
#   ?item a <http://example.org/phone_knowledge_graph.owl#Item> ;
#         <http://example.org/phone_knowledge_graph.owl#has_procedure> ?procedure .
# }
# GROUP BY ?item
# HAVING (COUNT(?procedure) > 2)
# """

# # Execute the query
# query2_results = g.query(query2)

# # Process and print the formatted results
# for result in query2_results:
#     item = str(result[0]).split('#')[-1]  # Extract the item name from the URI
#     formatted_name = format_result(item)  # Format the name by replacing underscores
#     print(formatted_name, "has", result[1], "procedures")  # Print the item name with procedure count

# Query 1: Count procedures and get items with more than 10 procedures
query1 = """
SELECT ?item (COUNT(?procedure) AS ?procedureCount)
WHERE {
  ?item a <http://example.org/phone_knowledge_graph.owl#Item> ;
        <http://example.org/phone_knowledge_graph.owl#has_procedure> ?procedure .
}
GROUP BY ?item
HAVING (COUNT(?procedure) > 2)
"""

# Execute Query 1
query1_results = g.query(query1)

# Collect items that have more than 10 procedures
items_with_many_procedures = []
for result in query1_results:
    item = str(result[0]).split('#')[-1]  # Extract item name
    formatted_item = format_result(item)  # Format the item name
    procedure_count = result[1]  # Get the procedure count
    print(f"{formatted_item} has {procedure_count} procedures")
    
    # Store the items
    items_with_many_procedures.append(result[0])

# Convert item URIs to SPARQL values format
item_uris = ' '.join(f"<{item}>" for item in items_with_many_procedures)

# Query 2: Get the procedures for the items found in Query 1
query2 = f"""
SELECT ?item ?procedure
WHERE {{
  ?item a <http://example.org/phone_knowledge_graph.owl#Item> ;
        <http://example.org/phone_knowledge_graph.owl#has_procedure> ?procedure .
  VALUES ?item {{ {item_uris} }}
}}
"""

# Execute Query 2 to get the procedures for the selected items
query2_results = g.query(query2)

# Process and print the results
for result in query2_results:
    item = str(result[0]).split('#')[-1]  # Extract item name
    procedure = str(result[1]).split('#')[-1]  # Extract procedure name
    formatted_item = format_result(item)
    formatted_procedure = format_result(procedure)
    print(f"Item: {formatted_item}, Procedure: {formatted_procedure}")

