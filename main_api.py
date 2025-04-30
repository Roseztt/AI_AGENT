from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag_query import query_rag
from fastapi.middleware.cors import CORSMiddleware

#create API
app = FastAPI(
    title="RAG AI_AGENT",
    description="RAG Agent that look through data in a Chroma Database",
)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True, 
    allow_methods=["*"],    
    allow_headers=["*"],   
)

#request model for querying RAG needs a user query input
class QueryRequest(BaseModel):
    query_text: str
    top_k: int = 10

#Query respond model with optional source that tells the user where the LLM get the answer from
class QueryResponse(BaseModel):
    response: str

#API path that  uses the response model to run a query
@app.post("/query/", response_model=QueryResponse)

#Sends in the user query through API following the request model
def execute_query(request: QueryRequest):
    query_text = request.query_text
    k = request.top_k

    if query_text == "":
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    
    response_text = query_rag(query_text=query_text)
    
    return QueryResponse(response=response_text)

@app.get("/")
def root():
    return {"Successfully connected to AI Agent, code: 200"}


