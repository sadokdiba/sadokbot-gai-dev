import requests
import argparse
import json
import os
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)  # Ensure the logs directory exists
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "chatbot.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Function to call the API
def make_api_call(api_key, text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "parts": [{"text": text}]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an error for HTTP issues
        
        # Log API call
        logging.info(f"API Request: {json.dumps(data)}")
        logging.info(f"API Response: {response.text}")
        
        return response.json()
    except requests.exceptions.RequestException as e:
        error_message = {"error": str(e)}
        logging.error(f"API Error: {error_message}")
        return error_message

# Extract the chatbot response text
def extract_text(response):
    try:
        # Navigate to the text part of the response
        return response["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError) as e:
        logging.error(f"Error extracting text: {str(e)}")
        return "Sorry, I couldn't process that."

# Main program logic
def main():
    parser = argparse.ArgumentParser(description="Interactive chatbot for API calls.")
    parser.add_argument("--api_key", required=False, help="Your API key for the generative language API")
    args = parser.parse_args()
    
    # Use API key from arguments or .env file
    api_key = args.api_key or os.getenv("API_KEY")
    if not api_key:
        print("API key is required. Please set it using --api_key or in the .env file.")
        return
    
    print("Interactive Chatbot (Type 'exit' to quit)\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        response = make_api_call(api_key, user_input)
        if "error" in response:
            print("Error:", response["error"])
        else:
            # Extract and display only the chatbot text response
            bot_response = extract_text(response)
            print("Sadok Bot:", bot_response)

if __name__ == "__main__":
    main()
