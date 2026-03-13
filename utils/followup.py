import json

def generate_followup_questions(chat_model, user_message: str, bot_response: str) -> list:
    try:
        from langchain_core.messages import HumanMessage
        prompt = f"""Based on this customer support conversation, suggest exactly 3 short follow-up questions the user might want to ask next.
Return ONLY a JSON array of 3 strings, nothing else. Example: ["Question 1?", "Question 2?", "Question 3?"]

User asked: {user_message}
Bot answered: {bot_response}

JSON array:"""
        response = chat_model.invoke([HumanMessage(content=prompt)])
        text = response.content.strip()
        start = text.find("[")
        end   = text.rfind("]") + 1
        if start != -1 and end != 0:
            return json.loads(text[start:end])[:3]
        return []
    except Exception as e:
        print(f"[Followup] Error: {e}")
        return []
