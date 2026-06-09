import json
import os
import urllib.request
from datetime import datetime
from http.server import BaseHTTPRequestHandler


def fetch_ai_news():
    api_key = os.environ.get("GROQ_API_KEY", "")
    today = datetime.now().strftime("%B %d, %Y")

    prompt = f"""Today is {today}. Return ONLY a valid JSON array with exactly 10 AI news objects. No markdown, no code fences, no explanation. Just the raw JSON array starting with [ and ending with ].

Each object must have these exact keys:
- title: a real recent AI news headline
- source: publication name like TechCrunch, The Verge, Wired, VentureBeat, Bloomberg
- summary: exactly 2 sentences about the story
- url: a real URL to that publication
- tag: exactly one of these words: Research, Industry, Models, Policy, Products, Startups
- featured: true for the most important story, false for all others

Cover topics like: new AI models, research papers, company news, AI regulation, product launches."""

    data = json.dumps({
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 3000,
        "temperature": 0.7
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=data,
        method="POST"
    )
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Bearer {api_key}")

    with urllib.request.urlopen(req, timeout=30) as response:
        result = json.loads(response.read().decode("utf-8"))

    text = result["choices"][0]["message"]["content"].strip()
    start = text.find("[")
    end = text.rfind("]") + 1
    return json.loads(text[start:end])


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            articles = fetch_ai_news()
            body = json.dumps({
                "date": datetime.now().strftime("%B %d, %Y"),
                "articles": articles
            })
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "s-maxage=3600")
            self.end_headers()
            self.wfile.write(body.encode("utf-8"))
        except Exception as e:
            error_body = json.dumps({"error": str(e)})
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(error_body.encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
