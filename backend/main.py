import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ollama
from tavily import TavilyClient
from youtubesearchpython import VideosSearch
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

class SearchRequest(BaseModel):
    query: str

def determine_intent(query: str) -> str:
    q = query.lower().strip()
    research_triggers = [
        "explain", "what is", "how to", "why does", "calculus", 
        "tutorial", "derive", "theory", "difference between", 
        "teach me", "guide", "concept"
    ]
    if any(trigger in q for trigger in research_triggers):
        return "ai"
    return "web"

def get_youtube_results(query: str):
    try:
        videos = VideosSearch(query, limit=4).result()["result"]
        if videos:
            return [{"title": v["title"], "url": v["link"]} for v in videos]
    except Exception as e:
        print("YouTube Search Error:", e)
    
    # FALLBACK: If YouTube library fails or blocks, generate reliable direct educational links
    return [
        {"title": f"Introduction to {query} on YouTube", "url": f"https://www.youtube.com/results?search_query={query}"},
        {"title": f"{query} Crash Course Tutorial", "url": f"https://www.youtube.com/results?search_query={query}+tutorial"}
    ]

@app.post("/api/generative-search")
async def search(req: SearchRequest):
    query = req.query
    intent = determine_intent(query)
    
    web_results = []
    image_results = []
    context_text = ""

    # Fetch live text AND images via Tavily Search API
    try:
        tavily_response = tavily_client.search(query=query, max_results=5, include_images=True)
        
        # 1. Parse Web Results
        for result in tavily_response.get("results", []):
            web_results.append({
                "title": result.get("title", "No Title Specified"),
                "url": result.get("url", "https://google.com"),
                "snippet": result.get("content", "")
            })
        context_text = " ".join([r["title"] + " " + r["snippet"] for r in web_results])
        
        # 2. Parse Live Real Images from Tavily!
        raw_images = tavily_response.get("images", [])
        if raw_images:
            for img in raw_images[:4]:
                # Handle dictionary or raw string formats seamlessly
                img_url = img.get("url") if isinstance(img, dict) else img
                if img_url:
                    image_results.append({"url": img_url})
                    
    except Exception as e:
        print("Tavily Error Extraction Exception:", e)

  
  
    answer = ""
    if intent == "ai":
        try:
            ai_res = ollama.chat(
                model="llama3",
                messages=[{
                    "role": "user",
                    "content": f"You are Gemini. Explain this topic elegantly with crisp layouts, paragraphs, and lists:\nQuery: {query}\nContext: {context_text}"
                }]
            )
            answer = ai_res["message"]["content"]
        except:
            answer = "AI generation node failed to synthesize payload."

    return {
        "intent": intent, 
        "answer": answer,
        "web_results": web_results,
  
        "followups": [
            f"Core foundational frameworks of {query}",
            f"Practical implementations of {query}"
        ]
    }
