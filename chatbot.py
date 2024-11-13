import google.generativeai as genai

#genai.configure(api_key = "Gemini-API-KEY")

genai.configure(api_key = "AIzaSyDX0ygCaZuU-XyMVICBQr17PtFSqKxGCfs")


import mesop as me
import mesop.labs as mel
import re
import json

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
    system_instruction = "You are an all purpose chatbot",
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

def load_keywords():
    with open("keywords.json", "r") as f:
        keywords = json.load(f)
    return keywords["female_keywords"], keywords["greetings"]#, keywords["female_references"]

female_keywords, greetings = load_keywords()
#female_references

def filter_query(query):
    query = query.lower()
    for keyword in female_keywords:
        if keyword in query:
            return "relevent"
        
    female_related_pattern = r"women|female|girl|lady|woman"
    if re.search(female_related_pattern, query.lower()):
        return "relevent"
    
    # for references in female_references:
    #     if references in query:
    #         return "relevent"

    for greeting in greetings:
        if greeting in query:
            return "relevent"
    return "irrelevent"

def transform(input: str, history: list[mel.ChatMessage]):
    query_type = filter_query(input)
    if query_type == "relevent":
        response = model.generate_content(input, stream=True)
        for chunk in response:
            yield chunk.text
    else:
        yield "I can only assist with queries related to female health and wellbeing."

'''
import json

def load_keywords():
    with open("keywords.json", "r") as f:
        keywords = json.load(f)
    return keywords["female_keywords"], keywords["greetings"]

female_keywords, greetings = load_keywords()

def filter_query(query):
    query = query.lower()
    for keyword in female_keywords:
        if keyword in query:
            return "female_health"

    for greeting in greetings:
        if greeting in query:
            return "greeting"
    return "irrelevent"
'''

'''
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
'''

'''
def transform(input: str, history: list[mel.ChatMessage]):
    response = model.generate_content(input, stream = True)

    for chunk in response:
        yield chunk.text
'''
