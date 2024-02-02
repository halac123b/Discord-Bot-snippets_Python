import discord
import os

client = discord.Client()


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
    # Pattern các câu lệnh
    if message.content.startswith("$hello"):
        # Gửi msg trả lời
        await message.channel.send("Hello!")


client.run(os.getenv("TOKEN"))
