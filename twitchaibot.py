# === Standard Imports ===

from twitchio.ext import commands, routines
import requests
import json
from datetime import datetime
from twitchio.ext.commands.errors import CommandNotFound
from dotenv import load_dotenv
import os

# === Load .env file === #
load_dotenv(dotenv_path=".env")  

# === Bot Configurations === #

BOT_NAME = os.getenv("BOT_NAME")
CLIENT_ID = os.getenv("CLIENT_ID")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_NAME1 = os.getenv("CHANNEL_NAME1")
CHANNEL_NAME2 = os.getenv("CHANNEL_NAME2")

# === OpenRouter API === #

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
REFERER_URL = os.getenv("REFERER_URL")
MODEL = os.getenv("MODELNAME")

# === Ignore or blocklist === #
# Get and parse ignored users
ignored_users_raw = os.getenv("IGNORED_USERS", "")
IGNORED_USERS = {user.strip() for user in ignored_users_raw.split(",") if user.strip()}

# === Injected Context from File === #
FILENAME = os.getenv("FILENAME")
if not FILENAME:
    raise ValueError("❌ FILENAME is not set in the .env file.")

try:
    with open(FILENAME, "r", encoding="utf-8") as f:
        CONTEXT_TEXT = f.read().strip()
except FileNotFoundError:
    print("⚠️ Warning: [filename].txt' not found. Continuing without injected context.")
    CONTEXT_TEXT = ""

# === Bot Class === #

class TwitchAIBot(commands.Bot):
    print(f"Loaded CHANNEL_NAME2: {CHANNEL_NAME2}")
    def __init__(self):
        super().__init__(token=BOT_TOKEN, prefix="!", initial_channels=[CHANNEL_NAME2])

    async def event_ready(self):
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ Logged in as | {self.nick}")
        await self.join_channels([CHANNEL_NAME2])
        print(f"Joined channels: {self.connected_channels}")
   
    async def event_command_error(self, context, error):
        if isinstance(error, CommandNotFound):
            return
        print(f"❌ Command error: {error}")
    
    async def event_message(self, message):
        if message.echo:
            return
        await self.handle_commands(message)

        username = message.author.name.lower()
        content_lower = message.content.lower().strip()

        if username in IGNORED_USERS:
            return
        
    @commands.command(name="gpt")
    async def gpt_command(self, ctx: commands.Context):
        username = ctx.author.name.lower()

        query = ctx.message.content[len("!gpt"):].strip()
        if not query:
            await ctx.send("Usage: !gpt [your question]")
            return
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] 💬 [GPT] @{ctx.author.name}: {query}")

        try:
            formatted_prompt = (
                f"You are helpful and informed assistant who knows a lot about Twitch Streamer {CHANNEL_NAME1} and their community"
                f"{CONTEXT_TEXT}\n\n"
                f"Answer the following user question as if you already know the info naturally"
                f"Do not mention about the context text file or say 'based on context'"
                f"User question: {query}\n\n"
                f"Respond in one sentence, 20 words or fewer. Be friendly, concise, and avoid anything harmful or inappropriate."
            )

            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": REFERER_URL,
                    "X-Title": BOT_NAME,
                },
                data=json.dumps({
                    "model": MODEL,
                    "messages": [{"role": "user", "content": formatted_prompt}]
                })
            )

            response_data = response.json()

            if "choices" not in response_data:
                print(f"[{timestamp}] ⚠️ GPT API returned an unexpected response:", response_data)
                await ctx.send("/me GPT error. Try again later!")
                return
            
            # === To limit the AI response to 35 words so that it doesn't take full space of chat screen === #
            reply = response_data["choices"][0]["message"]["content"].strip()
            word_count = len(reply.split())

            if word_count > 35:
                fallback_msg = (
                    "This question needs a longer answer than allowed. Try asking something shorter or more specific"
                )
                print(f"[{timestamp}] ⚠️ Skipped long response: {reply}")
                await ctx.send(f"@{ctx.author.name} {fallback_msg}")
                return
            
            print(f"[{timestamp}] 🤖 Response: {reply}")
            await ctx.send(f"@{ctx.author.name} {reply[:400]}")
        
        except Exception as e:
            print(f"[{timestamp}] GPT Error: {e}")
            await ctx.send("GPT error. Try again later.")

# === Run the Bot ===
bot = TwitchAIBot()
bot.run()       





