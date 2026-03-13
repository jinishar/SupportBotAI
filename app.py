import os, sys, tempfile, json
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from config.config import APP_TITLE, APP_ICON
from models.llm import get_groq_model
from utils.rag import build_vector_store, load_vector_store, retrieve_context
from utils.web_search import web_search
from utils.prompt_builder import build_system_prompt
from utils.translator import LANGUAGES, translate_text
from utils.followup import generate_followup_questions

st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout="wide")

# ── Session state ─────────────────────────────────────────────────────────────
defaults = {
    "messages": [],
    "vector_store": None,
    "docs_loaded": False,
    "followup_questions": [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

if st.session_state.vector_store is None:
    st.session_state.vector_store = load_vector_store()
    st.session_state.docs_loaded  = st.session_state.vector_store is not None

# ── Streaming response ────────────────────────────────────────────────────────
def stream_response(chat_model, messages, system_prompt):
    try:
        formatted = [SystemMessage(content=system_prompt)]
        for msg in messages:
            if msg["role"] == "user":
                formatted.append(HumanMessage(content=msg["content"]))
            else:
                formatted.append(AIMessage(content=msg["content"]))
        full_response = ""
        placeholder = st.empty()
        for chunk in chat_model.stream(formatted):
            token = chunk.content
            full_response += token
            placeholder.markdown(full_response + "▌")
        placeholder.markdown(full_response)
        return full_response
    except Exception as e:
        st.error(f"Error: {e}")
        return ""

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("SupportAI")
    st.caption("Powered by Groq · RAG · Web Search")
    st.divider()

    page = st.radio("Navigate", ["Chat", "Upload Documents", "Instructions"])
    st.divider()

    st.subheader("Language")
    selected_lang_name = st.selectbox("Response language:", list(LANGUAGES.keys()), index=0)
    selected_lang_code = LANGUAGES[selected_lang_name]

    st.subheader("Response Mode")
    response_mode = st.radio("Reply style:", ["Concise", "Detailed"], index=0)

    st.subheader("Live Web Search")
    use_web_search = st.toggle("Enable web search", value=False)

    st.divider()
    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.followup_questions = []
        st.rerun()

    st.caption(f"Docs: {'Loaded' if st.session_state.docs_loaded else 'None'}")
    st.caption(f"Web search: {'On' if use_web_search else 'Off'}")
    st.caption(f"Mode: {response_mode}")
    st.caption(f"Lang: {selected_lang_name}")

# ── Instructions ──────────────────────────────────────────────────────────────
if "Instructions" in page:
    st.title("How to Use SupportAI")
    st.markdown("""
## Setup
### 1. Install dependencies
```bash
pip install -r requirements.txt
```
### 2. Keys are already set in `config/config.py`
---
## Features
| Feature | How to use |
|---|---|
| **Chat** | Go to Chat and type your question |
| **RAG** | Upload docs in Upload, then ask questions about them |
| **Web Search** | Toggle in sidebar for live answers |
| **Response Mode** | Switch Concise / Detailed in sidebar |
| **Language** | Select response language in sidebar |
| **Follow-up** | Click suggested questions after each reply |
""")

# ── Upload Documents ──────────────────────────────────────────────────────────
elif "Upload" in page:
    st.title("Upload Knowledge Base Documents")
    st.markdown("Upload support documents (FAQs, manuals, policies). The bot will use them to answer questions.")

    uploaded_files = st.file_uploader(
        "Choose files (PDF, TXT, DOCX)",
        type=["pdf", "txt", "docx"],
        accept_multiple_files=True
    )

    if uploaded_files:
        if st.button("Process & Index Documents", type="primary"):
            with st.spinner("Indexing documents..."):
                try:
                    temp_paths = []
                    for uf in uploaded_files:
                        suffix = os.path.splitext(uf.name)[-1]
                        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                            tmp.write(uf.read())
                            temp_paths.append(tmp.name)
                    st.session_state.vector_store = build_vector_store(temp_paths)
                    st.session_state.docs_loaded  = True
                    for p in temp_paths:
                        try: os.unlink(p)
                        except: pass
                    st.success(f"Indexed {len(uploaded_files)} document(s) successfully!")
                except Exception as e:
                    st.error(f"Error: {e}")
    else:
        st.info("Upload files above then click Process & Index.")

    if st.session_state.docs_loaded:
        st.divider()
        st.success("Knowledge base active. Go to Chat to ask questions.")
        if st.button("Clear Knowledge Base"):
            import shutil
            from config.config import CHROMA_PERSIST_DIR
            shutil.rmtree(CHROMA_PERSIST_DIR, ignore_errors=True)
            st.session_state.vector_store = None
            st.session_state.docs_loaded  = False
            st.rerun()

# ── Chat ──────────────────────────────────────────────────────────────────────
else:
    st.title("SupportAI - Customer Support")
    st.caption("Ask me anything about our products, policies, or how to get help.")

    try:
        chat_model = get_groq_model()
    except ValueError as e:
        st.error(str(e))
        st.stop()

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Follow-up suggestions
    if st.session_state.followup_questions:
        st.markdown("**You might also want to ask:**")
        cols = st.columns(len(st.session_state.followup_questions))
        for col, q in zip(cols, st.session_state.followup_questions):
            with col:
                if st.button(q, use_container_width=True, key=f"fu_{q}"):
                    st.session_state.followup_questions = []
                    st.session_state.messages.append({"role": "user", "content": q})
                    st.rerun()

    # Chat input
    if prompt := st.chat_input("Type your question here..."):
        english_prompt = translate_text(prompt, "en") if selected_lang_code != "en" else prompt

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧑"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("SupportAI is typing..."):
                rag_context = retrieve_context(english_prompt, st.session_state.vector_store) if st.session_state.vector_store else ""
                web_context = web_search(english_prompt) if use_web_search else ""
                system_prompt = build_system_prompt(response_mode, rag_context, web_context)

            response = stream_response(chat_model, st.session_state.messages, system_prompt)

            if selected_lang_code != "en" and response:
                response = translate_text(response, selected_lang_code)
                st.markdown(response)

            badges = []
            if rag_context: badges.append("From your docs")
            if web_context: badges.append("Web search used")
            if selected_lang_code != "en": badges.append(f"{selected_lang_name}")
            if badges: st.caption(" · ".join(badges))

        st.session_state.messages.append({"role": "assistant", "content": response})

        st.session_state.followup_questions = generate_followup_questions(
            chat_model, english_prompt, response
        )
        st.rerun()