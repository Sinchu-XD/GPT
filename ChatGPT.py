import os
import openai
from telethon import TelegramClient, events
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

# Initialize Telegram bot client
bot = TelegramClient("chatgpt_bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Function to get ChatGPT response
def get_chatgpt_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Handle incoming messages
@bot.on(events.NewMessage)
async def handle_message(event):
    user_message = event.message.message
    chat_id = event.chat_id

    if user_message.startswith("/start"):
        await event.respond("🤖 Hello! I'm a ChatGPT-powered bot. Send me a message, and I'll reply!")
        return

    response = get_chatgpt_response(user_message)
    await event.respond(response)

# Start the bot
print("🤖 ChatGPT Telegram Bot is running...")
bot.run_until_disconnected()
