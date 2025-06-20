import os
import json
import datetime
import csv
import re
import numpy as np
import nltk
import ssl
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# --- SSL & NLTK Setup ---
ssl._create_default_https_context = ssl._create_unverified_context
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# --- Intent Loading ---
def load_intents(file_path='skill4future/intents.json'):
    try:
        with open(file_path, "r", encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        st.error(f"Error: Could not find intents file at {file_path}")
        return None

intents = load_intents()
if not intents:
    st.stop()

# --- Model Training ---
vectorizer = TfidfVectorizer()
clf = LogisticRegression(random_state=0, max_iter=10000)

tags = []
patterns = []
for intent in intents:
    for pattern in intent['patterns']:
        tags.append(intent['tag'])
        patterns.append(pattern)

x = vectorizer.fit_transform(patterns)
y = tags
clf.fit(x, y)

# --- Chatbot Logic ---
def chatbot(input_text):
    lower_input = input_text.lower().strip()

    # 1. Rule-based check for simple, high-frequency intents
    simple_intents = {
        'greeting': ['hi', 'hello', 'hey', 'good morning', 'good afternoon'],
        'goodbye': ['bye', 'goodbye', 'see you later', 'i have to go'],
        'thanks': ['thanks', 'thank you', "that's helpful"]
    }
    for tag, pattern_list in simple_intents.items():
        if lower_input in pattern_list:
            for intent in intents:
                if intent['tag'] == tag:
                    return intent['responses'][0]

    # 2. Rule-based check for math queries
    if re.search(r'\d\s*[\+\-\*\/\(\)]\s*\d', input_text):
        try:
            expression = "".join(re.findall(r'[\d\.\+\-\*\/ \(\)]', input_text))
            expression = expression.strip()
            if expression and any(char.isdigit() for char in expression):
                result = eval(expression, {"__builtins__": {}})
                return f"The result of {expression} is {result}."
        except (ZeroDivisionError, SyntaxError):
            pass

    # 3. Memory: Check for name introduction
    match = re.search(r'(?:my name is|i am|call me) (.*)', input_text, re.IGNORECASE)
    if match:
        name = match.group(1).strip()
        st.session_state.user_name = name
        return f"It's a pleasure to meet you, {name}!"

    # 4. ML-based intent classification with confidence threshold
    input_vec = vectorizer.transform([input_text])
    probabilities = clf.predict_proba(input_vec)
    max_prob = np.max(probabilities)
    
    CONFIDENCE_THRESHOLD = 0.7
    if max_prob > CONFIDENCE_THRESHOLD:
        tag = clf.predict(input_vec)[0]
        
        if tag == 'user_name':
            if st.session_state.get('user_name'):
                return f"I remember your name is {st.session_state.user_name}!"
            else:
                for intent in intents:
                    if intent['tag'] == 'user_name':
                        return intent['responses'][0]

        for intent in intents:
            if intent['tag'] == tag:
                return intent['responses'][0]
    
    # 5. Fallback response
    return "I'm not sure how to respond to that. You can ask me for a joke, to do some math, or about topics like health and education."

# --- Streamlit UI ---
if __name__ == '__main__':
    st.set_page_config(page_title="Chat with Bot", page_icon=":robot_face:")
    st.title("Chat with Bot 🤖")
    st.write("I'm Bot, your friendly conversational AI. I can chat with you, answer your questions, and even do some basic math. Let's talk!")

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "user_name" not in st.session_state:
        st.session_state.user_name = None

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What can I help you with?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = chatbot(prompt)
            st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Optional: Save to CSV log
        if not os.path.exists('chat_log.csv'):
            with open('chat_log.csv', 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['User Input', 'Chatbot Response', 'Timestamp'])
                
        timestamp = datetime.datetime.now().strftime(f"%Y-%m-%d %H:%M:%S")
        with open('chat_log.csv', 'a', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([prompt, response, timestamp])
