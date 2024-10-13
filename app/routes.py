# app/routes.py
from flask import request, jsonify, Blueprint, current_app, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('search.html')  # Render the search.html template

@main_bp.route('/query', methods=['POST'])
def query_graph():
    query = request.json.get('query')
    if not query:
        return jsonify({'error': 'No query provided'}), 400
     
    try:
        results = current_app.sparql_service.run_query(query)
        # Convert results to a list of dictionaries
        results_list = [{'subject': str(row[0]), 'predicate': str(row[1]), 'object': str(row[2])} for row in results]
        return jsonify(results_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
