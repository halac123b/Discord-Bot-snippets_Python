import discord
import os
import dotenv
import requests
import json
import random

dotenv.load_dotenv()

# Giống như các loại chatbot khác, cần khởi tạo intent kịch bản
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable"]
starter_encouragements = [
    "Cheer up!",
    "Hang in there.",
    "You are a great person / bot!",
]


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    # Parse response thành json
    json_data = json.loads(response.text)
    # Lấy quote và author từ json
    quote = json_data[0]["q"] + " -" + json_data[0]["a"]
    return quote


# On Bot Ready
@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


# On Message
@client.event
async def on_message(message):
    # Nếu là msg từ chính bot thì bỏ qua
    if message.author == client.user:
        return

    msg = message.content

    # Pattern các câu lệnh
    if msg.startswith("$hello"):
        # Gửi msg trả lời
        await message.channel.send("Hello!")

    if msg.startswith("$inspire"):
        quote = get_quote()
        await message.channel.send(quote)

    if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(starter_encouragements))


client.run(os.getenv("TOKEN"))
