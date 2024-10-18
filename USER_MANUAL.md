User Manual for Ontology-based Knowledge Graph Application:



1. Overview of the Ontology Schema

This ontology models the relationships between Items, Parts, Procedures, Tools, Steps, and Images. Key relationships include:

    Item: Represents a complete product (e.g., a phone).
    
    Part: Represents components or pieces of an item (e.g., a battery or screen).
    
    Procedure: Refers to a set of steps that outline how to repair or replace parts (e.g., "Battery Replacement").

    Sub-procedure (of a procedure): A procedure for the same item or a part of that item.
    
    Tool: Represents tools required for a procedure (e.g., a screwdriver or spudger).
    
    Step: Each procedure consists of multiple steps describing detailed actions.
    
    Image: Visual aids (like photos) associated with steps for clearer instructions.


    Item ↔ Part: An Item has Parts (e.g., a phone has a battery) using has_part / is_part_of.

    Item/Part ↔ Procedure: An Item or Part may have a Procedure associated with it (e.g., repair instructions) via has_procedure / is_procedure_for.

    Procedure ↔ Tool: A Procedure requires certain Tools through uses_tool / is_used_by.
    
    Procedure ↔ Step: Each Procedure contains multiple Steps with has_step / is_step_of.
    
    Step ↔ Image: Steps may be associated with an Image (e.g., a picture for better instruction).
    
    Procedure ↔ Sub-Procedure: Procedures can have nested or related procedures through has_sub_procedure / is_sub_procedure_of.

Schema Diagram Summary

    Classes: Item, Part, Procedure, Tool, Step, Image.
    Properties:
        Object Properties: has_part, is_part_of, has_procedure, uses_tool, has_step, etc.
        Datatype Properties: step_text (for instructions), mentioned_tools (tools listed in a step).

2. Example Queries

Here are some example SPARQL queries to help you interact with the knowledge graph:

1. Retrieve all parts of an item (e.g., a phone):


```
SELECT DISTINCT ?part 
WHERE {
  ?item a <http://example.org/phone_knowledge_graph.owl#Item> .
  ?item <http://example.org/phone_knowledge_graph.owl#has_part> ?part .
}
```
Interpretation: This query lists all the parts associated with items, such as the battery or screen of a phone.

2. List procedures related to a specific part (e.g., battery):

```
SELECT DISTINCT ?procedure 
WHERE {
  ?part a <http://example.org/phone_knowledge_graph.owl#Part> .
  ?part <http://example.org/phone_knowledge_graph.owl#has_procedure> ?procedure .
  FILTER CONTAINS(STR(?part), "Battery")
}
```

Interpretation: This query finds procedures like “Battery Replacement” for the given part.


3. Find tools used in a specific procedure (e.g., Screen Replacement):

```
SELECT ?tool 
WHERE {
  ?procedure a <http://example.org/phone_knowledge_graph.owl#Procedure> .
  ?procedure <http://example.org/phone_knowledge_graph.owl#uses_tool> ?tool .
  FILTER(CONTAINS(STR(?procedure), "Screen_Replacement"))
}
```

Interpretation: The result shows tools needed, such as a screwdriver.


4. Retrieve all steps and corresponding images for a procedure:

```
SELECT ?stepText ?image
WHERE {
  ?procedure a <http://example.org/phone_knowledge_graph.owl#Procedure> .
  ?procedure <http://example.org/phone_knowledge_graph.owl#has_step> ?step .
  ?step <http://example.org/phone_knowledge_graph.owl#step_text> ?stepText .
  OPTIONAL { ?step <http://example.org/phone_knowledge_graph.owl#has_image> ?image . }
  FILTER(CONTAINS(STR(?procedure), "Screen_Replacement"))
}
```

Interpretation: Lists steps for a procedure with associated images for better visualization.


3. Managing Data in the Knowledge Graph*******
Adding New Data



4. Adding or Modifying Ontology Rules*********
Adding New Rules

If you want to extend the ontology, you can add new rules using OWL.
Example: Add a new rule that every part must have at least one procedure:

```
<owl:Restriction>
  <owl:onProperty rdf:resource="#has_procedure"/>
  <owl:minCardinality rdf:datatype="http://www.w3.org/2001/XMLSchema#nonNegativeInteger">1</owl:minCardinality>
</owl:Restriction>
```

Updating Ontology Rules

    To update existing rules, modify the RDF/OWL XML file and re-upload it into the system. Ensure consistency with the existing schema to avoid conflicts.

    


1. Creating the Knowledge Graph

    Running the Scripts:
    Open your terminal and run the following commands to define the ontology and populate the knowledge graph:

    `python scripts/define_ontology.p`
    `python scripts/populate_ontology.py`

    This creates the ontology and knowledge graph files.


2. Using the web-application:

    Setting Up the Environment:
    From the `CITS3005-iFixit-Project` directory, install dependancies from terminal:
    `pip install -r requirements.txt`

    Then run the flask app
    `python run.py` 


3. Using Flask App:

    Use the navigation bar to navigate through the web page using the `Browse`, `Validate Data` and `Search` toggles:

    `Search`: Enter SPARQL queries or use predefined queries to explore the data. Note that The predefined queries will overwrite the SPARQL Query if both are inputted.

    `Browse`: View the items, procedures, and parts displayed on the browse page.
    
    `Validate Data`: Identify inconsistencies in tool usage and step descriptions.



7. Troubleshooting and FAQ

    Q: Why is my query not returning results?

        Verify that the entities and relationships you are querying exist in the graph.
        Adjust the query filters if necessary.

    Q: How do I restore the original ontology?

        Reload the original OWL/XML file into the knowledge graph system.

    Q: Can I extend the ontology with new classes?

        Yes, you can add new classes and properties to the OWL/XML file. Ensure they follow the existing structure to avoid conflicts.

8. Best Practices:

        Use Descriptive Labels: Ensure new items and procedures have meaningful names to simplify querying.
        Maintain Ontology Consistency: Follow schema rules when adding or modifying data.