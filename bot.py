import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import openai
import logging
from telegram.error import TimedOut

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from the .env file
load_dotenv()

# Retrieve the keys from the environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Function to generate response using OpenAI
def generate_response(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # You can use different OpenAI models
            prompt=prompt,
            max_tokens=100,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        logger.error(f"Error generating AI response: {e}")
        return "Oops! Something went wrong."

# Start command
def start(update: Update, context) -> None:
    update.message.reply_text("Hey! I'm Shruti, the bot that roasts and chats!")

# Handle text messages
def handle_text(update: Update, context) -> None:
    user_message = update.message.text
    response = generate_response(user_message)
    update.message.reply_text(response)

# Main function
def main():
    try:
        # Make sure the TELEGRAM_BOT_TOKEN is available in environment variables
        if not TELEGRAM_BOT_TOKEN:
            logger.error("TELEGRAM_BOT_TOKEN not found in environment variables!")
            print("Error: Telegram Bot Token is missing!")
            return

        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

        # Add handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

        # Run the bot with an increased timeout setting
        application.run_polling(timeout=20)  # Timeout set to 20 seconds
    except TimedOut as e:  # Added colon here
        logger.error("TimedOut error: Telegram bot connection timed out.")
        print("Timeout error! Check your internet connection.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        print("An unexpected error occurred. Check the logs for details.")

# Run the bot
if __name__ == "__main__":
    main()
