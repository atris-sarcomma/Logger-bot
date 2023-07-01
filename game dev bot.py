import discord
from discord import app_commands
from discord.ext import commands
import asyncio
intents = discord.Intents.default()
intents.members = True  # enable privileged intents
intents.typing = False
intents.presences = False
intents = discord.Intents.all()
client = commands.Bot(command_prefix='log ', intents=intents)  

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
    try:
        synced = await client.tree.sync()
        print(f'synced {len(synced)} commands')
    except Exception as e:
        print(e)
@client.tree.command(name='cool')
async def cool(interaction: discord.Interaction):
    await interaction.response.send_message(f'wao, {interaction.user.mention}') 

@client.command()
async def lat(ctx):
  await ctx.send(f'Pong! Latency{client.latency * 1000:.2f}')
  

@client.command()
async def clear(ctx, amount: int):
    channel = ctx.channel
    messages = []
    async for message in channel.history(limit=amount + 1):
        messages.append(message)
    await channel.delete_messages(messages)


@client.command()
async def delete(ctx, search_string: str):
    search_string = "Id: "+ search_string 
    channel = client.get_channel(1124351922015567882)
    messages = []
    async for message in channel.history(limit=None):
        if search_string in message.content:
            messages.append(message)
    await channel.delete_messages(messages)
    
@client.command()
async def find(ctx, search_string: str, note: str):
    search_string = "Title: "+ search_string 
    search_text = "Id: "+note.lower() 
    await ctx.send(search_string)
    channel = client.get_channel(1124351922015567882)
    async for message in channel.history(limit=None):
        if(search_string and search_text) in message.content:
            # Extract and print the message ID
            message_id = message.id
    find = await channel.fetch_message(message_id)
    await ctx.send(find.content)
    
@client.command()
async def read(ctx, message_id: int, note: str):
    try:
        channel = ctx.channel
        message = await channel.fetch_message(message_id)
        
        channel = client.get_channel(1124351922015567882)
        # Get the desired channel to save the message
        save_channel = client.get_channel(1124351922015567882)  # Replace YOUR_SAVE_CHANNEL_ID with the actual channel ID
        # Send the formatted message to the save channel
        await save_channel.send(f'Author: {message.author.name}\nTime: {message.created_at.strftime("%Y-%m-%d %H:%M:%S")}\nTitle: {note}\nId: {channel.topic}\nContent: \n ```{message.content}```')
 
        await ctx.send(f'Instance saved to {save_channel.mention}, message ID: {message_id}, Id: {channel.topic}')
        
        if channel.topic is not None:
            topic_int = int(channel.topic) + 1
            await channel.edit(topic=str(topic_int))
        else:
            await channel.edit(topic="1")
    except discord.NotFound:
        await ctx.send('Message not found.')
    except commands.MissingRequiredArgument as error:
        await ctx.send(f'Missing required argument: {error.param.name}')

client.run('Token')
