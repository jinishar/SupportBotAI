# SupportAI – Intelligent Customer Support Chatbot

A smart, context-aware customer support chatbot built with Streamlit, LangChain, and Groq LLM. The bot answers questions from uploaded documents (RAG), performs live web searches, supports multiple languages, and streams responses in real time.

---

## Features

| Feature | Description |
|---|---|
| **RAG (Retrieval-Augmented Generation)** | Upload PDF, TXT, or DOCX files and the bot answers from them |
| **Live Web Search** | Integrates Tavily API for real-time web answers |
| **Multi-language Support** | Responds in English, Hindi, Malayalam, Kannada, or German |
| **Streaming Responses** | Replies stream word by word like ChatGPT |
| **Follow-up Suggestions** | 3 clickable follow-up questions after every response |
| **Concise / Detailed Mode** | Switch between short answers and in-depth explanations |
| **Typing Animation** | "SupportAI is typing..." indicator while generating |

---

## Project Structure
```
AI_UseCase/
├── app.py                  ← Main Streamlit app
├── .env                    ← API keys (not committed)
├── requirements.txt
├── .streamlit/
│   └── config.toml         ← Theme config
├── config/
│   └── config.py           ← Settings and key loader
├── models/
│   ├── llm.py              ← Groq LLM setup
│   └── embeddings.py       ← HuggingFace embeddings
└── utils/
    ├── rag.py              ← Document loading, chunking, ChromaDB
    ├── web_search.py       ← Tavily web search
    ├── prompt_builder.py   ← Dynamic system prompt
    ├── translator.py       ← Multi-language translation
    └── followup.py         ← Follow-up question generation
```

---

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/jinishar/SupportBotAI.git
cd SupportBotAI
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your API keys

Create a `.env` file in the project root:
```
GROQ_API_KEY=your-groq-key-here
TAVILY_API_KEY=your-tavily-key-here
```

Get your keys from:
- Groq: https://console.groq.com (free)
- Tavily: https://app.tavily.com (free tier)

### 4. Run the app
```bash
streamlit run app.py
```

---

## How to Use

1. **Upload Documents** — Go to Upload Documents, upload a PDF/TXT/DOCX and click Process & Index
2. **Chat** — Go to Chat and start asking questions
3. **Web Search** — Toggle Enable web search in the sidebar for live answers
4. **Language** — Select your preferred response language from the sidebar
5. **Response Mode** — Switch between Concise and Detailed in the sidebar

---

## Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| LLM | Groq (LLaMA 3.1) |
| RAG | LangChain + ChromaDB |
| Embeddings | HuggingFace (all-MiniLM-L6-v2) |
| Web Search | Tavily API |
| Translation | Deep Translator (Google Translate) |

---

## Requirements

- Python 3.9+
- Internet connection (for Groq API, Tavily, and translation)
- Free API keys from Groq and Tavily

---

## Deployment

This app is deployed on Streamlit Cloud.

Live Demo: [SupportAI on Streamlit Cloud](https://supportbotai.streamlit.app/)
---

## Notes

- The `.env` file is excluded from the repository for security
- The `chroma_db` folder is auto-created locally when documents are indexed
- HuggingFace embedding model is downloaded on first run and cached locally
