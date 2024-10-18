# User Manual for Ontology-based Knowledge Graph Application:

## 1. Overview of the Ontology Schema

This ontology models the relationships between Items, Parts, Procedures, Tools, Steps, and Images. Below are the key components and their relationships:

#### Classes:

- **Item**: Represents a complete product (e.g., a phone).
  
- **Part**: Represents components or pieces of an item (e.g., a battery or screen).
  
- **Procedure**: Refers to a set of steps that outline how to repair or replace parts (e.g., "Battery Replacement").
  
- **Sub-procedure**: A procedure related to the same item or a part of that item.
  
- **Tool**: Represents tools required for a procedure (e.g., a screwdriver or spudger).
  
- **Step**: Each procedure consists of multiple steps describing detailed actions.
  
- **Image**: Visual aids (like photos) associated with steps for clearer instructions.

#### Relationships Between Classes:

- **Item ↔ Part**: An Item has Parts (e.g., a phone has a battery) using `has_part` / `is_part_of`.

- **Item/Part ↔ Procedure**: An Item or Part may have a Procedure associated with it (e.g., repair instructions) via `has_procedure` / `is_procedure_for`.

- **Procedure ↔ Tool**: A Procedure requires certain Tools through `uses_tool` / `is_used_by`.
  
- **Procedure ↔ Step**: Each Procedure contains multiple Steps with `has_step` / `is_step_of`.
  
- **Step ↔ Image**: Steps may be associated with an Image (e.g., a picture for better instruction) using `has_image` / `is_image_of`.
  
- **Procedure ↔ Sub-Procedure**: Procedures can have nested or related procedures through `has_sub_procedure` / `is_sub_procedure_of`.

#### Schema Summary:

- **Classes**: Item, Part, Procedure, Tool, Step, Image.

- **Object Properties**:
    - `has_part`: Relates an Item to its Parts.
    - `has_procedure`: Links Items or Parts to their associated Procedures.
    - `uses_tool`: Specifies the tools required for a Procedure.
    - `has_step`: Specifies the steps within a Procedure.
    - `has_image`: Links a Step to an Image for visual guidance.
    - `has_sub_procedure`: Indicates related or nested Procedures.

- **Data Properties**:
    - `step_text`: Contains text instructions for a step.
    - `mentioned_tools`: Lists tools mentioned in a step's description.

#### Example Use Case:
- For a phone with parts such as a battery and screen, the ontology links repair instructions (Procedures) to both the phone (Item) and the individual parts (Parts). Each procedure consists of several steps, each of which may include images and mention tools required to complete the repair.

- This structure allows querying for repair procedures, tools used, steps involved, and associated parts of an item.

## 2. Example Queries

Here are some example SPARQL queries to help you interact with the knowledge graph:

#### 1. Retrieve all parts of an item (e.g., a phone):

```
SELECT DISTINCT ?part 
WHERE {
  ?item a <http://example.org/phone_knowledge_graph.owl#Item> .
  ?item <http://example.org/phone_knowledge_graph.owl#has_part> ?part .
}
```
Interpretation: This query lists all the parts associated with items, such as the battery or screen of a phone.

#### 2. List procedures related to a specific part (e.g., battery):

```
SELECT DISTINCT ?procedure 
WHERE {
  ?part a <http://example.org/phone_knowledge_graph.owl#Part> .
  ?part <http://example.org/phone_knowledge_graph.owl#has_procedure> ?procedure .
  FILTER CONTAINS(STR(?part), "Battery")
}
```

Interpretation: This query finds procedures like “Battery Replacement” for the given part.


#### 3. Find tools used in a specific procedure (e.g., Screen Replacement):

```
SELECT ?tool 
WHERE {
  ?procedure a <http://example.org/phone_knowledge_graph.owl#Procedure> .
  ?procedure <http://example.org/phone_knowledge_graph.owl#uses_tool> ?tool .
  FILTER(CONTAINS(STR(?procedure), "Screen_Replacement"))
}
```

Interpretation: The result shows tools needed, such as a screwdriver.


#### 4. Retrieve all steps and corresponding images for a procedure:

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


## 3. Managing Data in the Knowledge Graph

### Adding New Data

To add new data to the knowledge graph, follow these steps:

#### 1. **Add new data to the JSON Data File (`Phone.json`)**:
   - All new data must be added to the `Phone.json` file in the `data/` directory.
   - Ensure that the new data includes details for Items, Parts, Procedures, Steps, and Tools.
   - Each entry should follow the same structure as the existing records in the JSON file. For example:
   
   ```json
   {
       "Title": "iPhone 12 Screen Replacement",
       "Category": "iPhone 12",
       "Toolbox": [
           {"Name": "screwdriver", "Url": "https://example.com/screwdriver"},
           {"Name": "spudger", "Url": "https://example.com/spudger"}
       ],
       "Steps": [
           {"Order": 1, "Text_raw": "Remove the screws with a screwdriver."},
           {"Order": 2, "Text_raw": "Use a spudger to pry open the case."}
       ],
       "Subject": "Screen"
   }
   ```

#### 2. Rerun the Scripts to Populate the Graph:

Once you’ve added data to the Phone.json file, rerun the population script to update the knowledge graph:

```
python scripts/populate_ontology.py
```

#### 3. Check for Errors:

Use the Validate Data option in the web application to ensure no inconsistencies exist in the populated data (e.g., tools not mentioned in steps).


### Modifying Existing Data

Modifying data in the knowledge graph follows a similar process to adding new data. If you need to update an existing record:

#### 1. Modify the JSON Data File:
   - Find the existing record you wish to modify in the `Phone.json` file.
   - For example, if you need to update the steps of a procedure, modify the `Steps` field as needed:
   
   ```json
   {
      "Title": "iPhone 12 Screen Replacement",
      "Category": "iPhone 12",
      "Toolbox": [
          {"Name": "screwdriver", "Url": "https://example.com/screwdriver"},
          {"Name": "spudger", "Url": "https://example.com/spudger"}
      ],
      "Steps": [
          {"Order": 1, "Text_raw": "Remove the screws with a screwdriver."},
          {"Order": 2, "Text_raw": "Use a spudger to pry open the case."},
          {"Order": 3, "Text_raw": "Remove the screen using a suction tool."}  // Modified step
      ],
      "Subject": "Screen"
   }
   ```

#### 2. Rerun the Scripts to Populate the Graph:

After making changes to the JSON file, rerun the population script:

```
python scripts/populate_ontology.py
```

#### 3. Validate the Changes:

Use the Validate Data option to check that the modifications have been applied correctly and there are no inconsistencies in the updated data.


### Deleting Data

To delete data from the knowledge graph, follow these steps:

#### 1. Remove the Entry from the JSON Data File:
   - Locate the entry (item, part, procedure) that you want to delete in the `Phone.json` file and remove it completely from the file
   - Example before deletion:

   ```json
   {
      "Title": "iPhone 12 Screen Replacement",
      "Category": "iPhone 12",
      "Toolbox": [
          {"Name": "screwdriver", "Url": "https://example.com/screwdriver"},
          {"Name": "spudger", "Url": "https://example.com/spudger"}
      ],
      "Steps": [
          {"Order": 1, "Text_raw": "Remove the screws with a screwdriver."},
          {"Order": 2, "Text_raw": "Use a spudger to pry open the case."}
      ],
      "Subject": "Screen"
   }
   ```

   - After deletion: Simply delete the entire entry for `iPhone 12 Screen Replacement`.

#### 2. Rerun the Population Script:

After removing the entry from the JSON file, rerun the population script to update the graph and reflect the deletion:

```
python scripts/populate_ontology.py
```

#### 3. Check for Inconsistencies:

Use the Validate Data option to ensure there are no leftover references to the deleted data in the knowledge graph (e.g., a procedure that referenced a deleted part).

#### 4. Alternative: Deleting Data Programmatically

- If you want to delete data programmatically (instead of manually removing it from the JSON file), modify the RDFLib graph by running custom Python scripts.

- Example Python code for deleting an individual from the knowledge graph:

```python
from rdflib import Graph, URIRef

# Load the knowledge graph
g = Graph()
g.parse("ontology/phone_knowledge_graph.owl")

# Define the URI of the individual to delete
individual_uri = URIRef("http://example.org/phone_knowledge_graph.owl#iPhone_12_Screen_Replacement")

# Remove all triples associated with the individual
g.remove((individual_uri, None, None))

# Save the updated graph
g.serialize(destination="ontology/phone_knowledge_graph.owl", format="xml")
```

- After running this script, rerun the web application or scripts to reflect the changes.



## 4. Adding or Modifying Ontology Rules*********
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

    


## 5. Creating the Knowledge Graph

    Running the Scripts:
    Open your terminal and run the following commands to define the ontology and populate the knowledge graph:

    `python scripts/define_ontology.p`
    `python scripts/populate_ontology.py`

    This creates the ontology and knowledge graph files.


## 6. Using the web-application:

    Setting Up the Environment:
    From the `CITS3005-iFixit-Project` directory, install dependancies from terminal:
    `pip install -r requirements.txt`

    Then run the flask app
    `python run.py` 


## 7. Using Flask App:

    Use the navigation bar to navigate through the web page using the `Browse`, `Validate Data` and `Search` toggles:

    `Search`: Enter SPARQL queries or use predefined queries to explore the data. Note that The predefined queries will overwrite the SPARQL Query if both are inputted.

    `Browse`: View the items, procedures, and parts displayed on the browse page.
    
    `Validate Data`: Identify inconsistencies in tool usage and step descriptions.



## 8. Troubleshooting and FAQ

    Q: Why is my query not returning results?

        Verify that the entities and relationships you are querying exist in the graph.
        Adjust the query filters if necessary.

    Q: How do I restore the original ontology?

        Reload the original OWL/XML file into the knowledge graph system.

    Q: Can I extend the ontology with new classes?

        Yes, you can add new classes and properties to the OWL/XML file. Ensure they follow the existing structure to avoid conflicts.

## 9. Best Practices:

        Use Descriptive Labels: Ensure new items and procedures have meaningful names to simplify querying.
        Maintain Ontology Consistency: Follow schema rules when adding or modifying data.