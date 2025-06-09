# 🤖 Chatbot using NLP

A simple yet powerful chatbot built with Python, NLTK, and Streamlit that uses Natural Language Processing (NLP) to understand and respond to user queries.

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Chatbot-using-NLP.git
   cd Chatbot-using-NLP
   ```

2. **Install the required packages**
   ```bash
   pip install -r requirements.txt
   ```
   
   If you don't have a requirements.txt file, install the packages manually:
   ```bash
   pip install nltk==3.8.1 scikit-learn==1.3.2 streamlit==1.31.0 numpy pandas
   ```

### 🏃‍♂️ Running the Application

1. **Navigate to the project directory**
   ```bash
   cd skill4future
   ```

2. **Run the Streamlit app**
   ```bash
   streamlit run chatbot.py
   ```

3. **Access the chatbot**
   The application will automatically open in your default web browser at:
   ```
   http://localhost:8501
   ```
   If it doesn't open automatically, you can manually navigate to the URL above.

## 🧪 Testing the Chatbot

1. Once the application is running, you'll see a text input field in your browser
2. Type a message like "Hi" or "Hello" and press Enter
3. The chatbot will respond based on the patterns in `intents.json`

### Example Interactions:
- User: "Hi"
- Bot: "Hello! How can I help you today?"

- User: "What can you do?"
- Bot: [Response from your intents.json]

## 🛠️ Customization

### Adding New Intents
1. Open `skill4future/intents.json`
2. Add a new intent object with patterns and responses:
   ```json
   {
     "tag": "greeting",
     "patterns": ["Hi", "Hello", "Hey there"],
     "responses": ["Hello!", "Hi there!", "Hey! How can I help you?"]
   }
   ```

## 📂 Project Structure

```
Chatbot-using-NLP/
├── skill4future/
│   ├── chatbot.py      # Main chatbot application
│   ├── intents.json    # Training data for the chatbot
│   └── nltk_data/      # NLTK data directory (will be created)
└── README.md           # This file
```

## 🤝 Contributing

Feel free to submit issues and enhancement requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Happy Chatting! 😊