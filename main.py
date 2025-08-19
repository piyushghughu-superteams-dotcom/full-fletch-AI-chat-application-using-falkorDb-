from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from db import execute_query
from llm import nl_to_cypher

app = FastAPI()

app.add_middleware( 
    CORSMiddleware,
    allow_origins=["*"],  #localhost://3000 charao aro sobai * connect korte parbe
    allow_credentials=True, #Allows cookies, authorization headers, etc
    allow_methods=["*"], #all methos like GET, POST, PUT etc.
    allow_headers=["*"], #Allow all types of headers to be sent in the request from frontend to backend
)


app.mount("/static", StaticFiles(directory="frontpart/build/static"), name="static")

@app.get("/")
def serve_react_index():
    return FileResponse("frontpart/build/index.html")

@app.post("/query")
async def query_handler(request: Request):
    data = await request.json()
    nl_query = data.get("query", "").strip()

    if not nl_query:
        return {
            "cypher": None,
            "result": [],
            "error": None,
            "message": "❗Please enter a valid question."
        }

    greetings = [
        "hi", "hello", "hey", "hii", "helloo", "yo", "what's up",
        "hola", "namaste", "sup", "greetings", "bonjour", "howdy"
    ]
    if any(greet in nl_query.lower() for greet in greetings):   
        return {
            "cypher": None,
            "result": [],
            "error": None,
            "message": "👋 Hi! What can I help you find in the database?"
        }

    try:
        cypher  = nl_to_cypher(nl_query)

        valid_starts = ("match", "create", "merge", "return")
        invalid_cypher = not cypher or not cypher.lower().startswith(valid_starts)
        if invalid_cypher:
            return {
                "cypher": cypher,
                "result": [],
                "error": None,
               "message": "❌ Couldn't understand your query.\n👋 Try asking something like: Show me all properties in Mumbai."
            }

        result = execute_query(cypher)
        return {"cypher": cypher, "result": result, "error": None}

    except Exception as e:
        return {
            "cypher": None,
            "result": [],
            "error": str(e),
            "message": "🚨 Something went wrong while processing your request."
        }
