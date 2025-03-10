import os
import openai
from telethon import TelegramClient, events
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
bot = TelegramClient("chatgpt_bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Function to get response from OpenAI
def get_chatgpt_response(message):
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": message}],
        )
        reply = response.choices[0].message.content.strip()

        # Ensure response is not empty
        if not reply:
            return "⚠️ I couldn't generate a response. Please try again."

        return reply
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Start command
@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    await event.respond("🤖 Hello! I'm a ChatGPT-powered bot. Send me a message, and I'll reply!")

# Handle messages
@bot.on(events.NewMessage)
async def chat(event):
    user_message = event.message.message

    # Prevent sending empty or invalid responses
    response = get_chatgpt_response(user_message)

    # Avoid formatting issues
    try:
        await event.respond(response, parse_mode="html")  # Ensures no formatting errors
    except:
        await event.respond("⚠️ Error sending the message. Please try again.")

# Start the bot
print("🤖 ChatGPT Telegram Bot is running...")
bot.run_until_disconnected()
