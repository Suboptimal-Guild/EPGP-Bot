#!/usr/bin/python
import argparse
import discord
import asyncio
import os

from commands.epgp import print_EPGP, print_EPGP_leaderboard, update_EPGP

# Constants
BOT_NAMES = [
    "Daddybot",
    "Fupabot",
    "Harambot 🍌",
    "Riggbot",
    "김정은",
    "Daddybot-dev",
    "Fupabot-Dev",
    "Harambot-Dev",
    "Riggbot-Dev",
    "김정은-Dev"
]

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message): # placeholder "bookmarks"
    # also we want to post messages in the channe lwhere the user asked, but
    # if possible make the message only viewable to them kinda like the default bot can do
    if message.author.name in BOT_NAMES:
        pass
    elif message.content.startswith('!epgp export') and is_officer(message.author):
        await update_EPGP(client, message)
    elif message.content.startswith('!epgp leaderboard'):
        await print_EPGP_leaderboard(client, message)
    elif message.content.startswith('!epgp'):
        await print_EPGP(client, message)

def is_officer(member):
    return (is_member_of_role(member, "Officers") or
    is_member_of_role(member, "Starlord") or
    is_member_of_role(member, "admin"))

def is_member_of_role(member, role_name):
    for role in member.roles:
        if role_name == role.name:
            return True
    return False

if __name__ == "__main__":
    '''
    Add two mutually exclusive commands, where one of the two is required for the
    script to run.
    '''
    parser = argparse.ArgumentParser(description="Flip a switch by setting a flag")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d','--dev',help="Run the bot in development mode.",action="store_true")
    group.add_argument('-p', '--prod',help="Run the bot in production mode.",action="store_true")
    args = parser.parse_args()

    client.accept_invite('https://discord.gg/mM5fXCe')

    if args.dev:
        client.run(os.environ['EPGP_BOT_DEVELOPMENT_TOKEN'])
    elif args.prod:
        client.run(os.environ['EPGP_BOT_PRODUCTION_TOKEN'])
    else:
        print("RIP in peace.")
