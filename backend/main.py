import asyncio
import requests
import ollama

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from qdrant_client import QdrantClient

app = FastAPI(title="Generative Search Engine API")


# CORS


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# QDRANT CONNECTION

qdrant_client = QdrantClient(
    host="localhost",
    port=6333
)


# REQUEST MODEL


class SearchRequest(BaseModel):
    query: str


# INTENT CLASSIFIER


def classify_intent(query: str) -> str:

    research_keywords = [
        "give me",
        "explain",
        "why",
        "how",
        "compare",
        "write",
        "summarize"
        "what is",
        "where is",
        "when does",
        "tutoriol",
        "guide",
        "tips",
        "ideas",
        "example",
        "history",
        "meaning",
        "case study",
        "documentation"
    ]

    query_lower = query.lower()
     
    if query_lower.startswitch("research"):
       return "Research"
 


    if any(keyword in query_lower for keyword in research_keywords):
        return "Research"
    
    return "Search"



# EMBEDDING FUNCTION


def get_embedding(text):

    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={
            "model": "nomic-embed-text",
            "prompt": text
        }
    )

    return response.json()["embedding"]


# QDRANT SEARCH


def search_documents(query):

    query_embedding = get_embedding(query)

    results = qdrant_client.query_points(
        collection_name="documents",
        query=query_embedding,
        limit=3
    )

    documents = []

    for point in results.points:
        documents.append(
            point.payload["text"]
        )

    return documents



# STREAMING GENERATOR

async def llama_stream_generator(prompt_text):

    try:

        response_stream = ollama.chat(
            model="llama3",
            messages=[
                {
                    "role": "user",
                    "content": prompt_text
                }
            ],
            stream=True
        )

        for chunk in response_stream:

            content = chunk["message"]["content"]

            if content:
                yield content
                await asyncio.sleep(0.01)

    except Exception as e:

        yield f"\nError: {str(e)}"


# MAIN ENDPOINT


@app.post("/api/generative-search")
async def generative_search(request: SearchRequest):

    if not request.query.strip():
        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty"
        )

    intent = classify_intent(request.query)

    
    # SEARCH MODE
    

    if intent == "Search":

        documents = search_documents(
            request.query
        )

        results = []

        for doc in documents:

            results.append(
                {
                    "title": doc,
                    "snippet": doc,
                    "url": "#"
                }
            )

        return {
            "intent": "Search",
            "results": results
        }

    
    # RESEARCH MODE (RAG)


    documents = search_documents(
        request.query
    )

    context = "\n".join(documents)
    prompt = f"""
     You are an expert research assistant.

     Use the provided context to answer the user's question.

     Context:
     {context}

     Question:
    {request.query}

     Generate a detailed research report using EXACTLY this format:

     # Overview
     Provide a short introduction.

     # Key Concepts
     Explain the main concepts.

     # Advantages
     List important advantages.

     # Disadvantages
     List limitations or drawbacks.

     # Applications
     Explain real-world use cases.

     # Conclusion
     Provide a concise conclusion.

     Keep the answer professional and well-structured.
     """
    return StreamingResponse(
        llama_stream_generator(prompt),
        media_type="text/plain"
    )


# ROOT


@app.get("/")
def root():

    return {
        "status": "running",
        "project": "Generative Search Engine"
    }


# RUN

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
