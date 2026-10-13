# 🎙️ Showrunner Agent — Tech & AI Talk Show Producer

An autonomous, multi-modal executive producer agent designed for modern **Tech & AI YouTube channels, podcasts, and livestreams**. Built with Google's **Agent Development Kit (ADK)** and powered by **Gemini 3.8 Flash**, Showrunner Agent plans complete episodes from cold-open hooks to technical deep dives, manages rundown pacing, generates high-CTR SEO packages, synthesizes 16:9 thumbnail cover art, and persists show branding across conversations with **Vertex AI Memory Bank**.

---

## 🌟 Key Features

- **⏱️ Algorithmic Episode Pacing (`calculate_episode_pacing`)**: Calculates precise segment timing (Cold Open, Tech Pulse, Deep Dive, Sponsor Read, Tool Showcase, Outro) adjusted to target runtime.
- **🔥 Trending AI Research Radar (`lookup_trending_ai_topics`)**: Curates angles on reasoning models, agent-to-agent (A2A) orchestration, test-time compute, and edge hardware deployment.
- **🚀 YouTube SEO & Engagement Suite (`generate_youtube_seo_pack`)**: Generates high-CTR title variations, community discussion hooks, tags, and pinned comment prompts.
- **🎨 16:9 Thumbnail Image Generation (`generate_episode_thumbnail_image`)**: Programmatically renders high-impact, dark cyber-neon episode cover art and hosts the assets directly on Google Cloud Storage.
- **🧠 Cross-Session Memory Bank**: Integrated with Vertex AI Memory Bank via `PreloadMemoryTool` and durable session write-back callbacks to retain show name, host persona, and guest history.
- **🖥️ A2UI v0.8 Rich Cards**: Emits structured Agent-to-UI JSON payloads rendering interactive cue cards and segment tables in compatible frontends.
- **🌐 A2A Protocol Native**: Deployed as an Agent Engine reasoning engine reachable via standard Agent-to-Agent (A2A) specifications.

---

## 🏗️ Architecture

```
User / Web Browser
       │
       ▼
Cloud Run Frontend (A2A Proxy + Web UI)
       │  (A2A Protocol / HTTP POST /chat)
       ▼
Vertex AI Agent Platform (Reasoning Engine)
       │
       ├─► Gemini 3.8 Flash (Core Reasoning & Planning)
       ├─► Custom Tools (Pacing, Trending AI Topics, SEO Suite)
       ├─► Visual Image Generator (Pillow / 16:9 Rendering)
       │         │
       │         └─► Google Cloud Storage (Public Thumbnail Bucket)
       │
       └─► Vertex AI Memory Bank (Long-Term Show Context)
```

---

## 📁 Repository Structure

```
showrunner-agent/
├── app/
│   ├── agent.py                 # Agent definition, Gemini model, callbacks, and tool wiring
│   ├── tools.py                 # Showrunner domain tools (pacing, AI trends, SEO pack)
│   ├── image_gen.py             # 16:9 thumbnail generation engine & GCS upload
│   ├── a2ui_prompt.py           # A2UI system instructions & formatting rules
│   ├── a2ui_utils.py            # A2UI callback transformer for A2A data parts
│   └── fast_api_app.py          # FastAPI local backend server
├── tests/
│   ├── integration/             # Integration tests for agent stream and server endpoints
│   └── unit/                    # Unit tests
├── pyproject.toml               # Python dependencies managed with uv
└── README.md                    # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- [Google Cloud SDK (gcloud)](https://cloud.google.com/sdk/docs/install)
- [google-agents-cli](https://pypi.org/project/google-agents-cli/)

### 1. Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/rahulkrishna493/buildwithgemini-showrunner-agent.git
cd buildwithgemini-showrunner-agent
uv sync
```

### 2. Environment Configuration

Create a `.env` file in the project root:

```bash
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_GENAI_USE_VERTEXAI=true
```

### 3. Run Locally

Launch the ADK development web interface:

```bash
uv run adk web --port 8080 --allow_origins "*" --reload_agents
```

Or run the interactive CLI:

```bash
agents-cli playground
```

### 4. Running Tests

Execute the automated test suite:

```bash
uv run --env-file .env pytest
```

---

## ☁️ Deployment

### Deploying to Vertex AI Agent Platform

Deploy the agent logic directly to Google Cloud Agent Runtime:

```bash
agents-cli deploy --project <your-project-id> --region us-central1
```

Once deployed, the CLI outputs your **Agent Runtime ID** and **Agent Card URL**.

---

## 💬 Sample Prompts

- *"I want to produce a 45-minute YouTube episode on Multi-Agent Systems and A2A protocols. Give me 3 title options and segment timing."*
- *"Generate an episode thumbnail image and title card for an episode on Autonomous AI Swarms."*
- *"We are interviewing a researcher on test-time compute. Draft 5 penetrating interview questions from foundational to spicy debate."*

---

## 📄 License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.
