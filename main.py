import discord
import os
import dotenv
import requests
import json
import random

# Package từ web IDE online Repl.it
from replit import db

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

if "responding" not in db.keys():
    db["responding"] = True


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    # Parse response thành json
    json_data = json.loads(response.text)
    # Lấy quote và author từ json
    quote = json_data[0]["q"] + " -" + json_data[0]["a"]
    return quote


def update_encouragements(encouraging_message):
    # Database của Replit được lưu dưới dạng key-value
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        # Add thêm câu encouraging_message vào list
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements
    # Nếu chưa có key "encouragements" thì tạo mới
    else:
        db["encouragements"] = [encouraging_message]


def delete_encouragment(index):
    """Xóa một câu encouraging_message từ list"""
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
    db["encouragements"] = encouragements


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

    # Nếu bot đang responding thì gửi encouraging_message
    if db["responding"]:
        options = starter_encouragements
        if "encouragements" in db.keys():
            options = options + db["encouragements"]

        if any(word in msg for word in sad_words):
            await message.channel.send(random.choice(options))

    # Add thêm câu encouraging_messageS
    if msg.startswith("$new"):
        # Xử lý string để lấy ra câu encouraging_message
        encouraging_message = msg.split("$new ", 1)[1]
        update_encouragements(encouraging_message)
        await message.channel.send("New encouraging message added.")

    if msg.startswith("$del"):
        encouragements = []
        if "encouragements" in db.keys():
            index = int(msg.split("$del", 1)[1])
            delete_encouragment(index)
            encouragements = db["encouragements"]
            await message.channel.send(encouragements)

    # Gửi list toàn bộ encouraging_message
    if msg.startswith("$list"):
        encouragements = []
        if "encouragements" in db.keys():
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)

    # Bật tắt responding
    if msg.startswith("$responding"):
        value = msg.split("$responding ", 1)[1]

        if value.lower() == "true":
            db["responding"] = True
            await message.channel.send("Responding is on.")
        else:
            db["responding"] = False
            await message.channel.send("Responding is off.")


client.run(os.getenv("TOKEN"))
