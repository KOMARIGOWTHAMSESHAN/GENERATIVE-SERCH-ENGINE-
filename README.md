# Full-Stack Local Generative Search Engine (RAG)

This is a full-stack, entirely local Generative Search Engine project. I am building this in modular sprints. Yesterday, I focused on getting the core FastAPI and Llama 3 streaming connection working. Today, I expanded the architecture by adding document chunking, an NLP intent classifier, a local Qdrant vector database running inside Docker, and a frontend built with Next.js.

The project is currently a work in progress, but the full-stack communication layer and the basic RAG pipeline are completely up and running.

---

##  Project Structure & Files

I have separated the project cleanly into two main directories to keep the backend logic and frontend UI completely independent:

###  Backend (/GENERATIVE_SEARCH_ENGINE-BACKEND)

This folder contains the Python scripts handling the data pipeline, database communication, and AI generation:
* main.py — The entry point for the FastAPI server that handles the streaming API endpoints.
* intent_classifier.py — A basic NLP routing script that checks what the user wants so the system can decide between standard search layouts or deep AI research.
* chunking.py & ingest.py — Scripts that split raw documents into clean, manageable text blocks.
* embed.py — Handles creating local vector embeddings from the text chunks.
* rag.py & search.py — The core logic that pulls matching context from the database and structures the final prompt for the LLM.
* store_documents.py & test_qdrant.py — Database scripts used to verify connections and save data inside the vector store.

###  Frontend (/GENERATIVE_SEARCH_ENGINE-FRONTEND)

A modern Next.js web application setup:
* app/page.tsx — My main interface file. It uses React hooks and fetch streams to catch the tokens coming from FastAPI and display them live on the screen with a smooth typewriter effect.


##  Tech Stack
* *Frontend:* Next.js (React), Node.js, TypeScript
* *Backend:* FastAPI (Python), Uvicorn
* *Vector Database:* Qdrant DB (Running locally via Docker)
* *Local LLM Engine:* Ollama running Llama 3


##  How to Run the App Locally

### 1. Run Qdrant Database
Make sure Docker Desktop is open, then start the Qdrant container:
```bash
docker run -p 6333:6333 qdrant/qdrant

### 2. Start Ollama
Make sure your local Ollama instance has the model ready :
```bash
ollama run llama3

### 3. Run the Backend
Open the terminal inside the backend directionary , activate the virtual environment install the requirements and boot up the server :
```bash
cd GENERATIVE_SEARCH_ENGINE-BACKEND
.\myenv\Scripts\Activate.ps1
pip install fastapi uvicorn pydantic ollama qdrant-client
python main.py

### 4. Run the Frontend
Open a separate terminal window , navigate to the frontend directiory,install the packaes and start the development server :
```bash
cd GENERATIVE_SEARCH_ENGINE-FRONTEND
npm install
npm run dev 

*Head to http://localhost:3000 to test the full app interface
