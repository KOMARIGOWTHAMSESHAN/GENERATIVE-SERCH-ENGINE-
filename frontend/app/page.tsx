"use client";

import { useState } from "react";

export default function Home() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState("");

  const handleSearch = async () => {
    setResult("Button Clicked Sucessfully");
    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/generative-search",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            query: query,
          }),
        }
      );

      const data = await response.json();

      setResult(JSON.stringify(data, null, 2));
    } catch (error) {
      setResult("Backend connection failed");
    }
  };

  return (
    <main className="min-h-screen p-10">
      <h1 className="text-4xl font-bold text-center mb-8">
        Generative Search Engine
      </h1>

      <div className="flex gap-2 max-w-3xl mx-auto">
        <input
          type="text"
          placeholder="Ask anything..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="border p-3 rounded-lg flex-1"
        />

        <button
          onClick={handleSearch}
          className="bg-black text-white px-5 rounded-lg"
        >
          Search
        </button>
      </div>

      <div className="max-w-3xl mx-auto mt-10 border rounded-lg p-5 whitespace-pre-wrap">
        {result || "Results will appear here"}
      </div>
    </main>
  );
}
