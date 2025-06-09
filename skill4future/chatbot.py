import os
import json
import datetime
import csv
import nltk
import ssl
import streamlit as st
import random
import joblib  # Added for model persistence
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# SSL context for NLTK downloads
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# NLTK data download
NLTK_DATA_DIR = os.path.join(os.path.dirname(__file__), 'nltk_data')
if not os.path.exists(NLTK_DATA_DIR):
    os.makedirs(NLTK_DATA_DIR)
nltk.data.path.append(NLTK_DATA_DIR)

try:
    nltk.data.find('tokenizers/punkt')
except nltk.downloader.DownloadError:
    nltk.download('punkt', download_dir=NLTK_DATA_DIR)
try:
    nltk.data.find('corpora/wordnet')
except nltk.downloader.DownloadError:
    nltk.download('wordnet', download_dir=NLTK_DATA_DIR)
try:
    nltk.data.find('corpora/omw-1.4')
except nltk.downloader.DownloadError:
    nltk.download('omw-1.4', download_dir=NLTK_DATA_DIR)

# Define model and vectorizer paths
MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)
VECTORIZER_PATH = os.path.join(MODEL_DIR, 'vectorizer.joblib')
CLF_PATH = os.path.join(MODEL_DIR, 'clf.joblib')

# Load intents from the JSON file
def load_intents():
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "intents.json"),
        os.path.join(os.getcwd(), "skill4future", "intents.json"),
        os.path.join(os.getcwd(), "intents.json"),
        "intents.json"
    ]
    for path in possible_paths:
        try:
            with open(path, "r", encoding='utf-8') as file:
                st.success(f"Loaded intents from: {os.path.abspath(path)}")
                return json.load(file)
        except FileNotFoundError:
            st.info(f"Intents file not found at: {os.path.abspath(path)}")
            continue
    st.error("Fatal Error: Could not find intents.json file after checking multiple paths.")
    return None

intents = load_intents()
if intents is None:
    st.stop()

# Load or train the model
if os.path.exists(VECTORIZER_PATH) and os.path.exists(CLF_PATH):
    st.info("Loading pre-trained model...")
    try:
        vectorizer = joblib.load(VECTORIZER_PATH)
        clf = joblib.load(CLF_PATH)
        st.success("Model loaded successfully!")
    except Exception as e:
        st.error(f"Error loading model: {e}. Retraining...")
        os.remove(VECTORIZER_PATH) # Remove potentially corrupted file
        os.remove(CLF_PATH) # Remove potentially corrupted file
        vectorizer = TfidfVectorizer()
        clf = LogisticRegression(random_state=0, max_iter=10000)
        # Preprocess and train
        tags = []
        patterns = []
        for intent_item in intents:
            for pattern in intent_item['patterns']:
                tags.append(intent_item['tag'])
                patterns.append(pattern)
        if not patterns: # Check if patterns is empty
            st.error("No patterns found in intents.json. Cannot train model.")
            st.stop()
        x = vectorizer.fit_transform(patterns)
        y = tags
        clf.fit(x, y)
        joblib.dump(vectorizer, VECTORIZER_PATH)
        joblib.dump(clf, CLF_PATH)
        st.success("Model retrained and saved!")
else:
    st.info("No pre-trained model found. Training new model...")
    vectorizer = TfidfVectorizer()
    clf = LogisticRegression(random_state=0, max_iter=10000)
    # Preprocess the data
    tags = []
    patterns = []
    for intent_item in intents:
        for pattern in intent_item['patterns']:
            tags.append(intent_item['tag'])
            patterns.append(pattern)
    
    if not patterns: # Check if patterns is empty
        st.error("No patterns found in intents.json. Cannot train model.")
        st.stop()

    # training the model
    x = vectorizer.fit_transform(patterns)
    y = tags
    clf.fit(x, y)
    # Save the trained model
    try:
        joblib.dump(vectorizer, VECTORIZER_PATH)
        joblib.dump(clf, CLF_PATH)
        st.success("Model trained and saved successfully!")
    except Exception as e:
        st.error(f"Error saving model: {e}")


def chatbot(input_text):
    input_text = vectorizer.transform([input_text])
    tag = clf.predict(input_text)[0]
    for intent in intents:
        if intent['tag'] == tag:
            response = random.choice(intent['responses'])
            return response
        
counter = 0

def main():
    global counter
    st.title("Intents of Chatbot using NLP")

    # Create a sidebar menu with options
    menu = ["Home", "Conversation History", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    # Home Menu
    if choice == "Home":
        st.write("Welcome to the chatbot. Please type a message and press Enter to start the conversation.")

        CHAT_LOG_FILE = os.path.join(os.path.dirname(__file__), 'chat_log.csv')

        # Check if the chat_log.csv file exists, and if not, create it with column names
        try:
            if not os.path.exists(CHAT_LOG_FILE):
                with open(CHAT_LOG_FILE, 'w', newline='', encoding='utf-8') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow(['User Input', 'Chatbot Response', 'Timestamp'])
        except IOError as e:
            st.warning(f"Could not create or access chat log file: {e}")

        # Use Streamlit session state for a more robust counter
        if 'chat_counter' not in st.session_state:
            st.session_state.chat_counter = 0
        st.session_state.chat_counter += 1
        
        user_input = st.text_input("You:", key=f"user_input_{st.session_state.chat_counter}")

        if user_input:
            user_input_str = str(user_input)
            response = chatbot(user_input_str) # Pass string to chatbot function
            st.text_area("Chatbot:", value=response, height=120, max_chars=None, key=f"chatbot_response_{st.session_state.chat_counter}")

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            try:
                with open(CHAT_LOG_FILE, 'a', newline='', encoding='utf-8') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow([user_input_str, response, timestamp])
            except IOError as e:
                st.warning(f"Could not write to chat log file: {e}")

            if response and response.lower() in ['goodbye', 'bye']:
                st.write("Thank you for chatting with me. Have a great day!")
                # Consider if st.stop() is desired here or if it should allow further interaction.

    # Conversation History Menu
    elif choice == "Conversation History":
        CHAT_LOG_FILE = os.path.join(os.path.dirname(__file__), 'chat_log.csv')
        st.header("Conversation History")
        try:
            if os.path.exists(CHAT_LOG_FILE):
                with open(CHAT_LOG_FILE, 'r', encoding='utf-8') as csvfile:
                    csv_reader = csv.reader(csvfile)
                    header = next(csv_reader, None)  # Skip the header row, handle empty file
                    if header:
                        history_data = list(csv_reader)
                        if not history_data:
                            st.info("No conversation history yet.")
                        else:
                            for row in reversed(history_data): # Show newest first
                                if len(row) == 3:
                                    st.text(f"User: {row[0]}")
                                    st.text(f"Chatbot: {row[1]}")
                                    st.text(f"Timestamp: {row[2]}")
                                    st.markdown("---")
                                else:
                                    st.warning("Skipping malformed row in chat history.")
                    else:
                        st.info("Chat log is empty or header is missing.")
            else:
                st.info("No conversation history file found.")
        except IOError as e:
            st.error(f"Could not read chat log file: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred while displaying chat history: {e}")

    elif choice == "About":
        st.write("The goal of this project is to create a chatbot that can understand and respond to user input based on intents. The chatbot is built using Natural Language Processing (NLP) library and Logistic Regression, to extract the intents and entities from user input. The chatbot is built using Streamlit, a Python library for building interactive web applications.")

        st.subheader("Project Overview:")

        st.write("""
        The project is divided into two parts:
        1. NLP techniques and Logistic Regression algorithm is used to train the chatbot on labeled intents and entities.
        2. For building the Chatbot interface, Streamlit web framework is used to build a web-based chatbot interface. The interface allows users to input text and receive responses from the chatbot.
        """)

        st.subheader("Dataset:")

        st.write("""
        The dataset used in this project is a collection of labelled intents and entities. The data is stored in a list.
        - Intents: The intent of the user input (e.g. "greeting", "budget", "about")
        - Entities: The entities extracted from user input (e.g. "Hi", "How do I create a budget?", "What is your purpose?")
        - Text: The user input text.
        """)

        st.subheader("Streamlit Chatbot Interface:")

        st.write("The chatbot interface is built using Streamlit. The interface includes a text input box for users to input their text and a chat window to display the chatbot's responses. The interface uses the trained model to generate responses to user input.")

        st.subheader("Conclusion:")

        st.write("In this project, a chatbot is built that can understand and respond to user input based on intents. The chatbot was trained using NLP and Logistic Regression, and the interface was built using Streamlit. This project can be extended by adding more data, using more sophisticated NLP techniques, deep learning algorithms.")

if __name__ == '__main__':
    main()
