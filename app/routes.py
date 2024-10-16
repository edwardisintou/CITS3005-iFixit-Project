from flask import request, jsonify, Blueprint, current_app, render_template

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
@main_bp.route('/query', methods=['POST'])
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
@main_bp.route('/validate')
def validate_data():
    g = current_app.sparql_service.graph
    query = """
    SELECT ?procedure ?tool
    WHERE {
        ?procedure a <http://example.org/phone_knowledge_graph.owl#Procedure> ;
                   <http://example.org/phone_knowledge_graph.owl#uses_tool> ?tool .
        FILTER NOT EXISTS {
            ?step <http://example.org/phone_knowledge_graph.owl#mentioned_tools> ?tool .
        }
    }
    """
    results = g.query(query)
    errors = [{"procedure": str(row[0]).split('#')[-1], "tool": str(row[1]).split('#')[-1]} for row in results]
    return render_template('errors.html', errors=errors)
