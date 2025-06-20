# 🤖 Chatbot using NLP

An intelligent and reliable chatbot built with Python, NLTK, and Streamlit. This project uses Natural Language Processing (NLP) to deliver dynamic, human-like conversations, perform calculations, and remember user details within a session.

## ✨ Key Features

- **Modern UI**: A clean, chat-style interface built with Streamlit.
- **Intelligent Responses**: Moves beyond static replies with a hybrid model that combines rule-based logic and machine learning (Logistic Regression) for higher accuracy.
- **Math Solver**: Can detect and accurately solve basic math expressions.
- **Session Memory**: Remembers the user's name during a conversation for a personalized experience.
- **Reliable & Deterministic**: Uses a confidence threshold to avoid irrelevant answers and provides a helpful fallback message.
- **Conversation Logging**: Saves chat history to a `chat_log.csv` file for review.

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Suhail-Ul-Hassan/Chatbot-using-NLP-main.git
   cd Chatbot-using-NLP-main
   ```

2. **Install the required packages**
   ```bash
   pip install -r requirements.txt
   ```

### 🏃‍♂️ Running the Application

1. **Run the Streamlit app**
   ```bash
   streamlit run skill4future/chatbot.py
   ```

2. **Access the chatbot**
   The application will open in your browser. Interact with the chatbot by typing in the input box.

## 🧪 Example Interactions

- **Greeting**: "Hello"
- **Math**: "what is 5*5"
- **Memory**: "my name is Alex"
- **Recall**: "what is my name?"
- **General**: "Tell me about education"

## 🛠️ Customization

### Adding New Intents

1. Open `skill4future/intents.json`.
2. Add a new intent object with a unique `tag`, a list of `patterns` (user queries), and a list of `responses`.

   ```json
   {
     "tag": "your_new_intent",
     "patterns": ["What is...", "Tell me about..."],
     "responses": ["This is the answer."]
   }
   ```
3. The model will automatically retrain with the new data when you restart the application.

## 📂 Project Structure

```
Chatbot-using-NLP-main/
├── skill4future/
│   ├── chatbot.py      # Main Streamlit application & chatbot logic
│   └── intents.json    # Training data (intents and responses)
├── chat_log.csv        # Stores conversation history (auto-generated)
├── requirements.txt    # Project dependencies
└── README.md           # This file
```

## 🤝 Contributing

Feel free to submit issues and enhancement requests.

---

Happy Chatting! 😊