import json
import os
import urllib.request
from datetime import datetime

def handler(request):
    try:
        api_key = os.environ.get("GROQ_API_KEY", "")
        today = datetime.now().strftime("%B %d, %Y")

        prompt = f"""Today is {today}. Return ONLY a valid JSON array with exactly 10 AI news objects. No markdown, no code fences. Each object needs: title, source, summary (2 sentences), url, tag (Research/Industry/Models/Policy/Products/Startups), featured (true for top story only)."""

        data = json.dumps({
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 3000
        }).encode("utf-8")

        req = urllib.request.Request(
            "https://api.groq.com/openai/v1/chat/completions",
            data=data, method="POST"
        )
        req.add_header("Content-Type", "application/json")
        req.add_header("Authorization", f"Bearer {api_key}")

        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))

        text = result["choices"][0]["message"]["content"].strip()
        articles = json.loads(text[text.find("["):text.rfind("]")+1])

        body = json.dumps({"date": today, "articles": articles})
        return Response(body, headers={"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"})

    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=500, headers={"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"})
