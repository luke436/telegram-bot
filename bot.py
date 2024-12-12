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
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Function to generate response using OpenAI
def generate_response(user_message):
    try:
        # Prepare the conversation history
        messages = [
            {"role": "system", "content": "You are Shruti, a funny, mean, and edgy bot that roasts people in group chats."},
            {"role": "user", "content": user_message}
        ]

        # Call OpenAI to get a response based on the conversation history
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can adjust the model
            messages=messages
        )

        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        logger.error(f"Error generating AI response: {e}")
        return "Oops! Something went wrong."

# Start command
async def start(update: Update, context) -> None:
    await update.message.reply_text("Hey! I'm Shruti, the bot that roasts and chats! "
                                    "I don't hold back, and I will roast you if you ask for it! "
                                    "Ready to chat?")

# Handle text messages
async def handle_text(update: Update, context) -> None:
    user_message = update.message.text
    response = generate_response(user_message)
    await update.message.reply_text(response)

# Main function
async def main():
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
        await application.run_polling(timeout=20)  # Timeout set to 20 seconds
    except TimedOut as e:  # Added colon here
        logger.error("TimedOut error: Telegram bot connection timed out.")
        print("Timeout error! Check your internet connection.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        print("An unexpected error occurred. Check the logs for details.")

# Run the bot
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
