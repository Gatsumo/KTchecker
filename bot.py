# Standard library imports
import os
import socket

# Third-party imports
import discord
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve token
TOKEN = os.getenv("DISCORD_TOKEN")

# Current known Kel'Thuzad IPs
KELTHUZAD_IPS = [
    '66.40.176.214',
    '66.40.179.208'
]

PORT = 3724
REALM_STATUS_URL = 'https://worldofwarcraft.blizzard.com/en-us/game/status/us'

# Create bot with command tree for Slash support
intents = discord.Intents.default()
bot = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(bot)

# TCP connection test
def check_tcp_connection(ip, port, timeout=3):
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except Exception:
        return False

# Scrape Blizz realm status
def scrape_realm_status(realm_name='Kel\'Thuzad'):
    try:
        response = requests.get(REALM_STATUS_URL, timeout=5)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.find_all('div', class_='RealmStatus--row')

        for row in rows:
            name_div = row.find('div', class_='RealmStatus--name')
            status_div = row.find('div', class_='RealmStatus--status')

            if name_div and status_div:
                name = name_div.text.strip()
                status = status_div.text.strip()

                if realm_name.lower() in name.lower():
                    return status

        return 'Unknown'
    except Exception as e:
        print(f'[ERROR] Failed to scrape realm status: {e}')
        return 'Error'

# Bot ready event
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')
    try:
        synced = await tree.sync()
        print(f'Synced {len(synced)} slash command(s).')
    except Exception as e:
        print(f'[ERROR] Slash sync failed: {e}')

# Slash command
@tree.command(name="ktstatus", description="Check Kel'Thuzad realm status (TCP + Blizzard site).")
async def ktstatus(interaction: discord.Interaction):
    await interaction.response.defer()

    tcp_responses = []
    for ip in KELTHUZAD_IPS:
        is_up = check_tcp_connection(ip, PORT)
        status = '🟢 UP' if is_up else '🔴 DOWN'
        tcp_responses.append(f'{ip}:{PORT} → {status}')

    blizz_status = scrape_realm_status()
    blizz_status_icon = '🟢' if blizz_status.lower() == 'up' else '🔴' if blizz_status.lower() == 'down' else '❓'

    response_message = '\n'.join(tcp_responses)
    response_message += f'\n\n**Blizzard Realm Status:** {blizz_status_icon} {blizz_status}'

    await interaction.followup.send(f'**Kel\'Thuzad Realm Check:**\n{response_message}')

# Run bot
bot.run(TOKEN)