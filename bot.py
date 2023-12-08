import discord
from discord.ext import commands
import requests
import lxml
import re
from bs4 import BeautifulSoup
import config


url = 'https://raw.githubusercontent.com/IceQ1337/CS-RSS-Feed/master/feeds/updates-feed-en.xml'

def run_discord_bot(client):
    @client.event
    async def on_ready():
        print('Logged in as: {}'.format(client.user.name))
        print('User ID: {}'.format(client.user.id))
        print('----------')

    @client.event
    async def on_message(message):
        if message.author.name == client.user.name:
            return

# test case for running message funciton
        if message.content.startswith('!update'):
            feed = get_html_and_parse(url)
            await message.channel.send(feed)


def get_html_and_parse(url):
    # Send a GET request to the URL and get the HTML content
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, "xml")
        entries = soup.find_all("item")

        if entries:
            latest_entry = entries[0]

            description = latest_entry.find("description")

            if description:
                description_text = description.get_text()

                description_soup = BeautifulSoup(description_text, 'html.parser')


                plain_text = description_soup.get_text(separator='\n')
                
                lines = plain_text.split('\n')
                formatted_lines = []
                for line in lines:
                    # Match all [ HEADINGS ]
                    if re.match("^\s*\[[^\]]*\].*", line):
                        formatted_lines.append(line) 
                    else:
                        formatted_lines.append("- " + line)



               # for line in lines:
               #     # Match all [ HEADINGS ]
               #     if re.match("^\s*\[[^\]]*\].*", line):
               #         print(line)
               #     else:
               #         print("- " + line)
            else:
                print("No description found in the latest entry.")
        else:
            print("No entries found in the RSS feed.")
    else:
        print(f"Failed to fetch the HTML. Status code: {response.status_code}")
    # lines = trans
    shift = "\n".join(formatted_lines)
    return shift


# run bot
if __name__ == '__main__':
#    api_key = (config.DISCORD_API)
    try:

        intents = discord.Intents.all()
        intents.message_content = True
        bot = commands.Bot(command_prefix="!",intents=intents)
        client = discord.Client(intents=intents)

        run_discord_bot(client)
        client.run(config.discord_token)

    except SystemExit:
        print('Shutting down :/')

