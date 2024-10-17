from flask import request, jsonify, Blueprint, current_app, render_template

main_bp = Blueprint('main', __name__)

# List of predefined queries
PREMADE_QUERIES = {
    "query1": {
        "description": "Find all procedures with more than 6 steps",
        "sparql": """
            SELECT DISTINCT ?procedure (COUNT(?step) AS ?stepCount)
            WHERE {
              ?procedure rdf:type <http://example.org/phone_knowledge_graph.owl#Procedure> .
              ?procedure <http://example.org/phone_knowledge_graph.owl#has_step> ?step .
            }
            GROUP BY ?procedure
            HAVING (COUNT(?step) > 6)
        """
    },
    "query2": {
        "description": "Find all items that have more than 10 procedures written for them",
        "sparql": """
            SELECT DISTINCT ?item (COUNT(?procedure) AS ?procedureCount)
            WHERE {
              ?item a <http://example.org/phone_knowledge_graph.owl#Item> ;
                    (<http://example.org/phone_knowledge_graph.owl#has_procedure> | <http://example.org/phone_knowledge_graph.owl#has_part_procedure>) ?procedure .
            }
            GROUP BY ?item
            HAVING (COUNT(?procedure) > 10)
        """
    },
    "query3": {
        "description": "Find all procedures that include a tool that is never mentioned in the procedure steps",
        "sparql": """
            SELECT DISTINCT ?procedure ?tool
            WHERE {
              ?procedure a <http://example.org/phone_knowledge_graph.owl#Procedure> ;
                         <http://example.org/phone_knowledge_graph.owl#unmentioned_tools> ?tool .
            }
        """
    },
    "query4": {
        "description": "Flag potential hazards in the procedure by identifying steps with words like 'careful' and 'dangerous'",
        "sparql": """
            SELECT DISTINCT ?procedure ?step ?stepText
            WHERE {
              ?procedure a <http://example.org/phone_knowledge_graph.owl#Procedure> ;
                         <http://example.org/phone_knowledge_graph.owl#has_step> ?step .
              
              ?step <http://example.org/phone_knowledge_graph.owl#step_text> ?stepText .
              
              FILTER(CONTAINS(LCASE(?stepText), "careful") || CONTAINS(LCASE(?stepText), "dangerous"))
            }
        """
    }
}

# Function to format the result by replacing underscores with spaces
def format_result(name):
    return name.replace('_', ' ')

def unformat_result(name):
    return name.replace(' ', '_')

# Home route: browse all items, its procedures and parts
@main_bp.route('/')
def browse_graph():
    g = current_app.sparql_service.graph
    
    # Query for items and their related procedures and parts
    query_items = """
    SELECT DISTINCT ?item ?procedure ?part
    WHERE {
      ?item a <http://example.org/phone_knowledge_graph.owl#Item> .
      OPTIONAL { ?item (<http://example.org/phone_knowledge_graph.owl#has_procedure> | <http://example.org/phone_knowledge_graph.owl#has_part_procedure>) ?procedure . }
      OPTIONAL { ?item <http://example.org/phone_knowledge_graph.owl#has_part> ?part . }
    }
    """
    
    results = g.query(query_items)
    
    # Data structure to store the items and their related procedures and parts
    data = {}
    
    for row in results:
        item = format_result(str(row[0]).split('#')[-1])
        procedure = format_result(str(row[1]).split('#')[-1]) if row[1] else None
        part = format_result(str(row[2]).split('#')[-1]) if row[2] else None

        # Initialize the item in the dictionary if not already present
        if item not in data:
            data[item] = {'procedures': set(), 'parts': set()}

        # Add procedures and parts to the item
        if procedure:
            data[item]['procedures'].add(procedure)
        if part:
            data[item]['parts'].add(part)

    return render_template('browse.html', data=data)

# Procedure route: details of a procedure
@main_bp.route('/procedure/<procedure>', methods=['GET'])
def procedure_details(procedure):
    g = current_app.sparql_service.graph
    
    # Revert the readable procedure name back to its original form with underscores
    original_procedure = unformat_result(procedure)

    # SPARQL query to retrieve the procedure's details and step text where available
    query_procedure = f"""
    SELECT DISTINCT ?class ?relation ?value ?stepText
    WHERE {{
      <http://example.org/phone_knowledge_graph.owl#{original_procedure}> a ?class .
      OPTIONAL {{ <http://example.org/phone_knowledge_graph.owl#{original_procedure}> ?relation ?value . }}
      OPTIONAL {{ ?value <http://example.org/phone_knowledge_graph.owl#step_text> ?stepText . }}
    }}
    """

    results = g.query(query_procedure)

    # Define the priority for different relations
    relation_priority = {
        'type': 1,
        'has sub procedure': 2,
        'uses tool': 3,
        'unmentioned tools': 4,
        'has step': 5
    }

    # Format the results
    procedure_data = {'name': format_result(procedure), 'class': '', 'relations': []}
    seen_relations = set()  # Track seen relations to avoid duplicates

    for row in results:
        procedure_class = format_result(str(row[0]).split('#')[-1])
        relation = format_result(str(row[1]).split('#')[-1]) if row[1] else None
        value = format_result(str(row[2]).split('#')[-1]) if row[2] else None
        step_text = row[3] if row[3] else None  # Check for step_text

        if procedure_class:
            procedure_data['class'] = procedure_class
        if relation:
            # If it's a step and there's readable text, prefer that over the identifier
            if relation == "has step" and step_text:
                value = step_text
            if value and (relation, value) not in seen_relations:
                procedure_data['relations'].append({'relation': relation, 'value': value})
                seen_relations.add((relation, value))  # Track the pair to prevent duplication

    # Sort relations by the predefined priority
    procedure_data['relations'].sort(key=lambda x: relation_priority.get(x['relation'], 99))  # Default to low priority if not in dict

    return render_template('procedure_details.html', procedure_data=procedure_data)

# Route to identify errors in the data (validation)
@main_bp.route('/validate', methods=['GET'])
def validate_errors():
    # Query for tools used but not mentioned in the procedure steps
    query = """
    SELECT DISTINCT ?procedure ?tool
    WHERE {
      ?procedure a <http://example.org/phone_knowledge_graph.owl#Procedure> ;
                 <http://example.org/phone_knowledge_graph.owl#unmentioned_tools> ?tool .
    }
    """
    try:
        # Run the query
        results = current_app.sparql_service.run_query(query)
        
        # Format and return the results
        formatted_results = []
        for result in results:
            procedure = str(result[0]).split('#')[-1]
            tool = str(result[1]).split('#')[-1]
            formatted_procedure = format_result(procedure)
            formatted_tool = format_result(tool)
            formatted_results.append({'procedure': formatted_procedure, 'tool': formatted_tool})

        # Render the results to the validation template
        return render_template('errors.html', errors=formatted_results)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Search route: allow search the graph by sparql queries
@main_bp.route('/search', methods=['GET', 'POST'])
def search_graph():
    g = current_app.sparql_service.graph

    if request.method == 'POST':
        # Get the selected premade query or custom SPARQL query from the user
        query_type = request.form.get('query_type')
        custom_query = request.form.get('custom_query')

        if query_type in PREMADE_QUERIES:
            query = PREMADE_QUERIES[query_type]['sparql']
            # Define headers based on the query
            if query_type == 'query1':
                headers = ['Procedure', 'Step Count']
            elif query_type == 'query2':
                headers = ['Item', 'Procedure Count']
            elif query_type == 'query3':
                headers = ['Procedure', 'Unmentioned Tool']
            elif query_type == 'query4':
                headers = ['Procedure', 'Step']
            else:
                headers = []
        elif custom_query:
            query = custom_query
            headers = []  # No headers for custom queries
        else:
            return jsonify({'error': 'No valid query provided'}), 400

        try:
            # Run the query
            results = g.query(query)

            # Format the results for query4 to only show Procedure and Step Text
            formatted_results = []
            if query_type == 'query4':  # Adjust formatting specifically for Query 4
                for result in results:
                    procedure = format_result(str(result[0]).split('#')[-1])  # Procedure
                    step_text = result[2]  # Actual step text
                    formatted_results.append([procedure, step_text])
            else:
                # Format results for other queries
                formatted_results = [
                    [format_result(str(val).split('#')[-1]) if val else '' for val in result]
                    for result in results
                ]

            # Pass both the headers and the results to the template
            return render_template('results.html', headers=headers, results=formatted_results)

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return render_template('search.html', premade_queries=PREMADE_QUERIES)
