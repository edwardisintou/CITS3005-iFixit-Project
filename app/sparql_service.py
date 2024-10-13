# app/sparql_service.py
from rdflib import Graph

class SparqlService:
    def __init__(self, ontology_path, knowledge_graph_path):
        self.graph = Graph()
        # Load the ontology and knowledge graph files
        self.graph.parse(ontology_path, format='xml')
        self.graph.parse(knowledge_graph_path, format='xml')

    def run_query(self, query):
        return self.graph.query(query)
