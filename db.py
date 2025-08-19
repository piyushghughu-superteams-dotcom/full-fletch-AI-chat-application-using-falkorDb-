from falkordb import FalkorDB
import os
from dotenv import load_dotenv

load_dotenv()

FALKORDB_HOST = os.getenv("FALKORDB_HOST", "localhost")
FALKORDB_PORT = int(os.getenv("FALKORDB_PORT", 6379))
GRAPH_NAME = os.getenv("FALKORDB_GRAPH", "PropertiesGraph")


client = FalkorDB(host=FALKORDB_HOST, port=FALKORDB_PORT)
graph = client.select_graph(GRAPH_NAME)

def execute_query(cypher_query: str):
    try:
        result = graph.query(cypher_query)
        return result.result_set
    except Exception as e:
        return {"error": str(e)}
