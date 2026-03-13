BASE_SYSTEM = """You are SupportAI, a friendly and knowledgeable customer support assistant.
Your job is to help users by answering their questions accurately and helpfully.
Always be polite, professional, and empathetic.
If you are unsure about something, say so honestly rather than guessing."""

CONCISE_INSTRUCTION = """
RESPONSE MODE: CONCISE — Keep answers short, 2-4 sentences. Prioritise clarity."""

DETAILED_INSTRUCTION = """
RESPONSE MODE: DETAILED — Provide thorough, well-structured answers with bullet points where helpful."""

def build_system_prompt(mode: str, rag_context: str = "", web_context: str = "") -> str:
    prompt = BASE_SYSTEM
    prompt += CONCISE_INSTRUCTION if mode == "Concise" else DETAILED_INSTRUCTION

    if rag_context.strip():
        prompt += f"\n\nKNOWLEDGE BASE CONTEXT:\n---\n{rag_context}\n---\nUse the above context to answer when relevant."

    if web_context.strip():
        prompt += f"\n\nLIVE WEB SEARCH RESULTS:\n---\n{web_context}\n---\nUse the above to supplement your answer."

    return prompt