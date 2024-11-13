import google.generativeai as genai

genai.configure(api_key = "Gemini-API-KEY")

import mesop as me
import mesop.labs as mel

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name = "gemini-1.5-flash",
    generation_config = generation_config,
    system_instruction = "You are Athena, a friendly and knowledgeable AI assistant, here to empower individuals, especially young women and people who want to understand the women in their lives, with accurate information and empathetic support. Your goal is to break down gender stereotypes and taboos, dispel myths, and foster a more compassionate and informed society with understanding between people. You must deny any other unrelated topics that is asked to you.",
)

safe = [
        {
            "category": "HARM_CATEGORY_DANGEROUS",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE",
        },
    ]

@me.page(
    security_policy = me.SecurityPolicy(
        allowed_iframe_parents = ["https://google.github.io"]
    ),
    path = "/chat",
    title = "Athena Chat",
)

def page():
    mel.chat(transform, title = "Athena Bot", bot_user = "Athena")

def transform(input: str, history: list[mel.ChatMessage]):
    response = model.generate_content(input, stream = True, safety_settings=safe)

    for chunk in response:
        yield chunk.text
