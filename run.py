#!/usr/bin/python
import argparse
import discord
import asyncio
import os

from commands.epgp import print_EPGP, print_EPGP_leaderboard, update_EPGP

client = discord.Client()

@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------")

@client.event
async def on_message(message): # placeholder "bookmarks"
    # Don't generate a message if it came from another bot. This may be added
    # later.
    if is_bot(message.author):
        pass
    # Easy check for if the bot is awake.
    elif message.content.startswith("!test"):
        await client.send_message(message.channel, "I\'m awake.")
    # Write updated EPGP information to the EPGP spreadsheet.
    elif message.content.startswith('!epgp export') and is_officer(message.author):
        await update_EPGP(client, message)
    # Print the EPGP leaderboard based on parameters such as armor type and stat.
    elif message.content.startswith('!epgp leaderboard'):
        await print_EPGP_leaderboard(client, message)
    # Print the full EPGP leaderboard.
    elif message.content.startswith('!epgp'):
        await print_EPGP(client, message)

def is_bot(member):
    return is_member_of_role(member, "botlords")

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
    group.add_argument("-d", "--dev", help="Run the bot in development mode.", action="store_true")
    group.add_argument("-p", "--prod", help="Run the bot in production mode.", action="store_true")
    args = parser.parse_args()

    if args.dev:
        client.run(os.environ["EPGP_BOT_DEVELOPMENT_TOKEN"])
    elif args.prod:
        client.run(os.environ["EPGP_BOT_PRODUCTION_TOKEN"])
    else:
        print("Error: Bot Environment Ambiguous")
