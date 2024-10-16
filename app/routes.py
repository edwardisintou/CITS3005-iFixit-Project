from flask import request, jsonify, Blueprint, current_app, render_template

# Function to format the result by replacing underscores with spaces
def format_result(name):
    return name.replace('_', ' ')

main_bp = Blueprint('main', __name__)

# Home route: browse all classes and individuals
@main_bp.route('/')
def browse_graph():
    g = current_app.sparql_service.graph
    query = """
    SELECT ?class ?individual
    WHERE {
        ?individual a ?class .
    }
    """
    results = g.query(query)
    data = [{"class": str(row[0]).split('#')[-1], "individual": str(row[1]).split('#')[-1]} for row in results]
    return render_template('browse.html', data=data)

# Route to execute SPARQL queries
@main_bp.route('/search', methods=['POST'])
def query_graph():
    query = request.form.get('query')
    if not query:
        return jsonify({'error': 'No query provided'}), 400

    try:
        results = current_app.sparql_service.run_query(query)
        formatted_results = [{"subject": str(row[0]), "predicate": str(row[1]), "object": str(row[2])} for row in results]
        return render_template('results.html', results=formatted_results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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