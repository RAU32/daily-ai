import json
import os
import urllib.request
from datetime import datetime
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            api_key = os.environ.get("GROQ_API_KEY", "")
            today = datetime.now().strftime("%B %d, %Y")
            prompt = f"Today is {today}. Return ONLY a JSON array with 10 AI news objects. No markdown. Each needs: title, source, summary (2 sentences), url, tag (Research/Industry/Models/Policy/Products/Startups), featured (true for #1 only)."
            data = json.dumps({"model":"llama-3.3-70b-versatile","messages":[{"role":"user","content":prompt}],"max_tokens":3000}).encode()
            req = urllib.request.Request("https://api.groq.com/openai/v1/chat/completions",data=data,method="POST")
            req.add_header("Content-Type","application/json")
            req.add_header("Authorization",f"Bearer {api_key}")
            with urllib.request.urlopen(req,timeout=30) as r:
                result = json.loads(r.read())
            text = result["choices"][0]["message"]["content"].strip()
            articles = json.loads(text[text.find("["):text.rfind("]")+1])
            body = json.dumps({"date":today,"articles":articles}).encode()
            self.send_response(200)
            self.send_header("Content-Type","application/json")
            self.send_header("Access-Control-Allow-Origin","*")
            self.end_headers()
            self.wfile.write(body)
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type","application/json")
            self.send_header("Access-Control-Allow-Origin","*")
            self.end_headers()
            self.wfile.write(json.dumps({"error":str(e)}).encode())
