import discord
import requests
import random
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.model import SlashCommandOptionType
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)

shown_urls = set()
MAX_SHOWN_URLS = 100

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@slash.slash(
    name="gawrgura",
    description="Get a random Gawr Gura fanart or video from the r/GawrGura subreddit",
)
async def get_gawr_gura_art(ctx):
    search_url = 'https://www.reddit.com/r/GawrGura/random.json'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    response = requests.get(search_url, headers=headers)
    found_image_or_video = False  # Add a variable to track whether an image or video was found
    if response.status_code == 200:
        post_data = response.json()[0]['data']['children'][0]['data']
        if 'url_overridden_by_dest' in post_data:
            url = post_data['url_overridden_by_dest']
            if url in shown_urls:
                await ctx.send("That image or video has already been shown.")
                return
            if len(shown_urls) >= MAX_SHOWN_URLS:
                shown_urls.pop()
            shown_urls.add(url)
            if url.endswith('.jpg') or url.endswith('.jpeg') or url.endswith('.png'):
                embed = discord.Embed(title=post_data['title'], url=f"https://www.reddit.com{post_data['permalink']}")
                embed.set_image(url=url)
                await ctx.send(embed=embed)
                found_image_or_video = True  # Set the variable to True if an image is found
            elif url.endswith('.gif') or url.endswith('.gifv') or url.endswith('.webm') or url.endswith('.mp4'):
                embed = discord.Embed(title=post_data['title'], url=f"https://www.reddit.com{post_data['permalink']}")
                embed.add_field(name="Video", value=url)
                await ctx.send(embed=embed)
                found_image_or_video = True  # Set the variable to True if a video is found
        if not found_image_or_video:  # Check if no image or video was found
            await ctx.send("No images or videos were found.")
    else:
        await ctx.send('No results found.')

@slash.slash(
    name="ping",
    description="Shows the latency of the bot",
)
async def ping(ctx):
    latency = bot.latency * 1000
    await ctx.send(f"Pong! Latency: {latency:.2f} ms")

bot.run('MTEwNjA2MjQ4Mzc0MDk1NDYzNA.Gq6Z-9.ITB8iqe98aXJYZ0OjrBCDLcGD1jjqSKm3jv-2A')
