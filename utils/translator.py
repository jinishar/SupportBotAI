LANGUAGES = {
    "English":   "en",
    "Hindi":     "hi",
    "Malayalam": "ml",
    "Kannada":   "kn",
    "German":    "de",
}

def translate_text(text: str, target_lang: str) -> str:
    if target_lang == "en" or not text.strip():
        return text
    try:
        from deep_translator import GoogleTranslator
        return GoogleTranslator(source="auto", target=target_lang).translate(text)
    except Exception as e:
        print(f"[Translator] Error: {e}")
        return text