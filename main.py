import discord
import requests
import random
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.model import SlashCommandOptionType
from discord.ext import commands
from bs4 import BeautifulSoup

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
    found_image_or_video = False
    while not found_image_or_video:
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

                    # Use the post title as a search query on Google Images
                    search_query = post_data['title']
                    google_images_url = f"https://www.google.com/search?q={search_query}&tbm=isch"
                    response = requests.get(google_images_url, headers=headers)

                    # Use Beautiful Soup to scrape the search results page and find the artist name (if available)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        artist_divs = soup.find_all('div', {'class': 'fKDtNb'})
                        if artist_divs:
                            artist_name = artist_divs[0].text
                            embed.set_footer(text=f"Original artist: {artist_name}")

                    await ctx.send(embed=embed)
                    found_image_or_video = True
                elif url.endswith('.gif') or url.endswith('.gifv') or url.endswith('.webm') or url.endswith('.mp4'):
                    embed = discord.Embed(title=post_data['title'], url=f"https://www.reddit.com{post_data['permalink']}")
                    embed.add_field(name="Video", value=url)
                    await ctx.send(embed=embed)
                    found_image_or_video = True
            if not found_image_or_video:
                response = requests.get(search_url, headers=headers)
        else:
            await ctx.send('No results found.')
            return
@slash.slash(
    name="ping",
    description="Shows the latency of the bot",
)
async def ping(ctx):
    latency = bot.latency * 1000
    await ctx.send(f"Pong! Latency: {latency:.2f} ms")

@slash.slash(
    name="trending",
    description="Shows the most popular posts on r/GawrGura",
)
async def trending(ctx):
    search_url = 'https://www.reddit.com/r/GawrGura/top.json?t=day&limit=100'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    response = requests.get(search_url, headers=headers)
    found_image_or_video = False
    while not found_image_or_video:
        if response.status_code == 200:
            json_data = response.json()
            post_data = random.choice(json_data['data']['children'])['data']
            if 'url_overridden_by_dest' in post_data:
                url = post_data['url_overridden_by_dest']
                if url in shown_urls:
                    continue
                if len(shown_urls) >= MAX_SHOWN_URLS:
                    shown_urls.pop()
                shown_urls.add(url)
                if url.endswith('.jpg') or url.endswith('.jpeg') or url.endswith('.png'):
                    embed = discord.Embed(title=post_data['title'], url=f"https://www.reddit.com{post_data['permalink']}")
                    embed.set_image(url=url)

                    # Use the post title as a search query on Google Images
                    search_query = post_data['title']
                    google_images_url = f"https://www.google.com/search?q={search_query}&tbm=isch"
                    response = requests.get(google_images_url, headers=headers)

                    # Use Beautiful Soup to scrape the search results page and find the artist name (if available)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        artist_divs = soup.find_all('div', {'class': 'fKDtNb'})
                        if artist_divs:
                            artist_name = artist_divs[0].text
                            embed.set_footer(text=f"Original artist: {artist_name}")

                    await ctx.send(embed=embed)
                    found_image_or_video = True
                elif url.endswith('.gif') or url.endswith('.gifv') or url.endswith('.webm') or url.endswith('.mp4'):
                    embed = discord.Embed(title=post_data['title'], url=f"https://www.reddit.com{post_data['permalink']}")
                    embed.add_field(name="Video", value=url)
                    await ctx.send(embed=embed)
                    found_image_or_video = True
            if not found_image_or_video:
                continue
        else:
            await ctx.send('No results found.')
            return

bot.run('MTEwNjA2MjQ4Mzc0MDk1NDYzNA.Gq6Z-9.ITB8iqe98aXJYZ0OjrBCDLcGD1jjqSKm3jv-2A')
