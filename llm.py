import os
import requests
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

SYSTEM_PROMPT = """
You are an expert at converting natural language into Cypher queries for FalkorDB.

The graph is named `PropertiesGraph` and contains nodes and relationships related to properties.

Rules:
- Only output a valid Cypher query.
- Do not explain anything.
- Do not add extra formatting or symbols.
- If the question cannot be mapped to Cypher, output only: INVALID_QUERY
"""

def nl_to_cypher(nl_query: str) -> str:
    body = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": nl_query}
        ],
        "temperature": 0.2
    }

    response = requests.post(GROQ_URL, headers=HEADERS, json=body)
    response.raise_for_status()

    cypher = response.json()["choices"][0]["message"]["content"].strip()
    return cypher
