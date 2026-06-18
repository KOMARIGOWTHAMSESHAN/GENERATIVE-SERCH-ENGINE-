import requests

def get_embedding(text):

    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={
            "model": "nomic-embed-text",
            "prompt" : text
        }
    )
    return response.json()["embedding"]

embedding = get_embedding(
    "FastAPI is a Python framework"
)
print("Vector Length:",len(embedding))
