
import os
import openai
from pyrogram import Client, filters
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI API
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Initialize Telegram bot
bot = Client("chatgpt_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Function to get response from OpenAI
def get_chatgpt_response(message):
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": message}],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Start command
@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("🤖 Hello! I'm a ChatGPT-powered bot. Send me a message, and I'll reply!")

# Handle messages
@bot.on_message(filters.text)
async def chat(client, message):
    response = get_chatgpt_response(message.text)
    await message.reply_text(response)

# Start the bot
bot.run()
