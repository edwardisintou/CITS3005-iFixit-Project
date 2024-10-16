from flask import Flask
from .sparql_service import SparqlService
from .routes import main_bp

def create_app():
    app = Flask(__name__)

    # Load the SparqlService with your OWL files
    ontology_path = "ontology/phone_ontology.owl"
    knowledge_graph_path = "ontology/phone_knowledge_graph.owl"
    app.sparql_service = SparqlService(ontology_path, knowledge_graph_path)

    # Register the blueprint for routes
    app.register_blueprint(main_bp)

    return app
