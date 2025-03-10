import os
import asyncio
from pyrogram import Client, filters
import openai

# Set up OpenAI API Key
OPENAI_API_KEY = "your_openai_api_key"
openai.api_key = OPENAI_API_KEY

# Telegram Bot credentials
API_ID = "your_api_id"
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"

# Initialize Pyrogram Client
app = Client("chatgpt_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Function to interact with OpenAI ChatGPT
def chat_with_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",  # Updated to latest model
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Handle /start command
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("🤖 Hello! I am a ChatGPT-4-powered bot. Ask me anything!")

# Handle user messages and respond with ChatGPT output
@app.on_message(filters.text & ~filters.command)
async def chat(client, message):
    user_message = message.text
    response = chat_with_gpt(user_message)
    await message.reply(response)

# Run the bot
async def main():
    await app.start()
    print("ChatGPT-4 Telegram Bot is running...")
    await idle()
    await app.stop()

if name == "main":
    asyncio.run(main())
