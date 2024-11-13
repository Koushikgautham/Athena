import google.generativeai as genai

genai.configure(api_key = "Gemini-API-KEY")

import mesop as me
import mesop.labs as mel
import re

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
    system_instruction = "You are a helpful assistant, you provide helpful answers, ",
)

@me.page(
    security_policy = me.SecurityPolicy(
        allowed_iframe_parents = ["https://google.github.io"]
    ),
    path = "/chat",
    title = "Athena Chat",
)

def page():
    mel.chat(transform, title = "Athena Bot", bot_user = "Athena")

def filter_query(query):
    female_related_keywords = ["women's health", "female health", "menstruation", "menopause",
                               "pregnancy", "birth control", "gynecology", "fertility", "periods"]

    for keyword in female_related_keywords:
        if keyword in query.lower():
            return "female_health"

    # Use regular expressions for more flexible matching
    female_related_pattern = r"women|female|girl|lady|woman"
    if re.search(female_related_pattern, query.lower()):
        return "female_health"

    # Check for basic greetings
    greeting_pattern = r"hey|hello|hi"
    if re.search(greeting_pattern, query.lower()):
        return "greeting"

    return "irrelevant"

def transform(input: str, history: list[mel.ChatMessage]):
    query_type = filter_query(input)

    if query_type == "female_health":
        response = model.generate_content(input, stream=True)
        for chunk in response:
            yield chunk.text
    elif query_type == "greeting":
        yield "Hello! How can I help you today?"
    else:
        yield "I can only assist with queries related to female health and wellbeing."

# def transform(input: str, history: list[mel.ChatMessage]):
#     response = model.generate_content(input, stream = True)

#     for chunk in response:
#         yield chunk.text
