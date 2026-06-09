# AI Pulse 🧠
> Daily AI news aggregator — powered by Claude + Web Search. Updates automatically every day.

## How It Works
Every time someone opens the app, it calls a Vercel serverless function (`/api/news`) which uses the Claude API with web search to fetch today's top 10 AI stories from trusted sources in real time. Results are cached for 1 hour so it's fast for repeat visitors.

---

## Deploy in 15 Minutes (Free)

### Step 1 — Get Your Anthropic API Key
1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Click **API Keys** → **Create Key**
3. Copy the key (starts with `sk-ant-...`)

### Step 2 — Upload to GitHub
1. Go to [github.com](https://github.com) → Sign in → Click **New repository**
2. Name it `ai-pulse` → Click **Create repository**
3. Upload all these files by dragging them into GitHub (or use GitHub Desktop)

Your file structure should look like:
```
ai-pulse/
├── api/
│   └── news.py
├── public/
│   └── index.html
├── requirements.txt
├── vercel.json
└── README.md
```

### Step 3 — Deploy on Vercel
1. Go to [vercel.com](https://vercel.com) → Sign up free with GitHub
2. Click **Add New Project** → Import your `ai-pulse` GitHub repo
3. Click **Deploy** (Vercel auto-detects the config)

### Step 4 — Add Your API Key
1. In Vercel dashboard → your project → **Settings** → **Environment Variables**
2. Add:
   - **Name:** `ANTHROPIC_API_KEY`
   - **Value:** your key from Step 1
3. Click **Save** → Go to **Deployments** → **Redeploy**

### Step 5 — Done! 🎉
Vercel gives you a free live URL like:
```
https://ai-pulse-yourname.vercel.app
```

Share this link anywhere. Every day, it automatically fetches fresh AI news.

---

## Tech Stack
- **Frontend:** Vanilla HTML/CSS/JS — Apple-style glassmorphism UI
- **Backend:** Python serverless function on Vercel
- **AI:** Claude API (`claude-opus-4-6`) with built-in web search
- **Hosting:** Vercel (free tier)
- **Cost:** ~$0.01–0.05 per page load (Anthropic API usage)

---

## Customisation
To change which sources are searched, edit the system prompt in `api/news.py`.
To change the UI colors or layout, edit `public/index.html`.

---

Built by Raushan Tiwari · BS Data Science & Applications, IIT Madras
