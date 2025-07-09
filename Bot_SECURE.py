import discord
from discord.ext import commands
import random
import yt_dlp
from asyncio import Queue
import requests
import asyncio
from newsapi import NewsApiClient
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

intents = discord.Intents.all()
intents.members = True
intents.guild_messages = True
intents.guild_reactions = True
bot = commands.Bot(command_prefix='!', intents=intents)

song_queue=Queue()
players = {}
newsapi = NewsApiClient(api_key=NEWS_API_KEY)
channel_id=1064973772098117747

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_message(message):
    print('Received message:', message.content)
    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="Members")
    await member.add_roles(role)
    channel = bot.get_channel(1065373097621979210)
    await channel.send(f"Bine ai venit {member.mention}, eu sunt Ilie Moromete, botul acestui server!")

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(1065373097621979210)
    await channel.send(f"De ce {member.display_name} a parasit server-ul? Ca sa se mire prostii de-aia!")

@bot.command(name='news')
async def news(ctx):
    top_headlines = newsapi.get_top_headlines(sources='bbc-news')
    headlines = []
    for article in top_headlines['articles']:
        headline = f"**{article['title']}**\n{article['description']}\nRead more: {article['url']}"
        headlines.append(headline)
    if headlines:
        message = '\n\n'.join(headlines)
        embed = discord.Embed(title='Latest news from BBC', description=message, color=discord.Color.blue())
        await ctx.send(embed=embed)
    else:
        await ctx.send('Nicio stire gasita.')

@bot.command(name='ping')
async def ping(ctx):
    print("Pong!")
    await ctx.send('Pong!')

@bot.command(name='echo')
async def echo(ctx, *, message):
    await ctx.send(message)

@bot.command(name='roll')
async def roll(ctx, dice: str):
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Continut invalid, te rog foloseste formatul NdN, e.g. 3d6.')
        return
    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command(name='play')
async def play(ctx, *, query):
    if not ctx.author.voice:
        return await ctx.send("Nu esti conectat la un canal de voce, mai intai te rog sa te conectezi la unu!")
    await song_queue.put(query)
    if not ctx.voice_client:
        voice_channel = ctx.author.voice.channel
        await voice_channel.connect()
    if ctx.voice_client.is_playing():
        return
    while not song_queue.empty():
        async with ctx.typing():
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'song.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            ffmpeg_options = {
                'options': '-vn -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
            }
            query = await song_queue.get()
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(query, download=False)
                url = info['url']
                title = info['title']
            vc = ctx.voice_client
            vc.play(discord.FFmpegPCMAudio(url, **ffmpeg_options), after=lambda e: print(f'Player error: {e}') if e else None)
            await ctx.send(f':musical_note: **Incepe: {title}** :musical_note:')
            while vc.is_playing() or vc.is_paused():
                await asyncio.sleep(1)
            await asyncio.sleep(1)

@bot.command(name='skip')
async def skip(ctx):
    voice_client = ctx.guild.voice_client
    if not voice_client or not voice_client.is_playing():
        return await ctx.send("There's nothing playing right now.")
    voice_client.stop()
    await ctx.send("Skipping the current song...")

@bot.command(name='leave')
async def stop(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client:
        try:
            voice_client.stop()
            await voice_client.disconnect()
            await ctx.send("Opresc melodia si ma voi deconecta de pe voice channel")
        except Exception as e:
            await ctx.send(f"An error occurred while stopping the song: {e}")
    else:
        await ctx.send("Nu sunt conectat la un canal de voce.")

@bot.command(name='weather')
async def weather(ctx, *, location):
    url = "https://api.openweathermap.org/data/2.5/weather?q=" + location + "&appid=" + WEATHER_API_KEY + "&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.HTTPError:
        return await ctx.send(f'Nu am putut gasi vremea pntru {location}')
    city = data['name']
    country = data['sys']['country']
    temperature = data['main']['temp']
    description = data['weather'][0]['description']
    flag = f':flag_{country.lower()}:'
    embed = discord.Embed(title=f'Vremea in {city}, {country}', color=0x00ff00)
    embed.add_field(name='Temperatura', value=f'{temperature} °C', inline=True)
    embed.add_field(name='Descriere a vremii ', value=description.capitalize(), inline=True)
    await ctx.send(embed=embed)

bot.run(DISCORD_TOKEN)