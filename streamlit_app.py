import os
import sys

# Add the skill4future directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import and run the main app
from skill4future.chatbot import main

if __name__ == "__main__":
    main()
