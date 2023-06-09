import json
import discord
import random
import requests
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import CommandNotFound
from discord.ext.commands import has_permissions
from discord.ext import tasks
from discord.utils import get
from apikeys import *
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
import bs4
import asyncio
import youtube_dl
import os
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
import collections
from collections import deque

#dhruva
role_id = 853960280924618772
user_id = 345189736723251201

#prefix and enabling all intents
bot = commands.Bot(command_prefix = '?', intents=discord.Intents.all())

#custom status shuffle
movies = ("Interstellar", "A Space Odyssey", "Pandorum", "Gravity", "Star Wars", "Guardians of the Galaxy", "Star Trek", "The Martian", "Rogue One",
"Rick and Morty", "The Mandalorian", "Futurama", "Alien", "Apollo 13", "The Transformers", "Firefly", "The Clone Wars")

#repeating custom status
@tasks.loop(seconds=60.0)
async def my_background_task():
    await bot.change_presence(activity=discord.Activity(type=3, name=random.choice(movies)))

#on ready
@bot.event
async def on_ready():
    print("Bot is up and ready!")

    #error testing
    try:
        synced = await bot.tree.sync()
        print("Synced")
    except Exception as e:
        print(e)

    #starts the custom status shuffle once the bot is online
    await bot.wait_until_ready()
    my_background_task.start()

#disconnect from all voice channels upon going offline
@bot.event
async def on_disconnect():
    for vc in bot.voice_clients:
        await vc.disconnect()
        
#welcome message
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name = 'welcome')
    embed = discord.Embed(title=f"Hello {member.name}!", description = f"Welcome to {member.guild.name}")
    await channel.send(embed=embed)

#leave message
@bot.event
async def on_member_leave(member):
    channel = discord.utils.get(member.guild.channels, name = 'welcome')
    embed = discord.Embed(title=f"Goodbye {member.name}", description="See you later") # F-Strings!
    await channel.send(embed=embed)

#cointoss
@bot.tree.command(name='toss')
async def toss(interaction: discord.Interaction):
    cointoss = random.randrange(2)
    if(cointoss == 1):
        await interaction.response.send_message("Tails!")
    else:
        await interaction.response.send_message("Heads!")


#rolldice
@bot.tree.command(name='roll')
async def roll(interaction: discord.Interaction):
    dice = random.randrange(7)
    await interaction.response.send_message(f"You rolled {dice}.")


#slash command 1 (help)
@bot.tree.command(name="help")
async def help(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention}! Message <@636940258239447062> on discord if you have any questions") 


#slash command 2 (info)
@bot.tree.command(name="info")
async def help(interaction: discord.Interaction):

    embed = discord.Embed(title="Features", description='''\n1. Welcomes members when they join the server. Will not work if there is no channel named 'welcome'.
    \n2. Roll and Flip - Rolls a dice or flips a coin.
    \n3. ?join and ?leave - makes the bot join or leave the voice channel you are currently in.
    \n4. ?avatar - displays user's avatar.
    \n5. ?prune - prunes the last x messages in the channel. Requires manage messages permission to work.
    \n6. ?play - pass song URL as parameter. Will stop the currently playing song and play the second one if used twice.
    \n7. ?pause, ?resume, ?stop - for music. (Music feature is currently unsupported. I am working on fixing this)\n''', color=0x0D47A1)

    embed.add_field(name="Written by", value="V1k1ng#6950", inline=False)

    await interaction.response.send_message(embed=embed)
    
#avatar
@bot.command()
async def avatar(ctx, user: discord.User = None):

    if user is None:
        user = ctx.author
    await ctx.send(user.avatar)

#dm
@bot.command()
async def dm(ctx, user: discord.User, *, content: str):

    if ctx.author.id == 636940258239447062:
        await user.send(content)
        await ctx.send(f"Sent a DM to {user}.", delete_after=5.0)
        await ctx.channel.purge(limit=2)

    else:
        await ctx.send("Unauthorized", delete_after=5.0)

#prune
@bot.command()
async def prune(ctx, amount: int):
    # Check if the user has the permission to manage messages
    author = ctx.author

    if author.guild_permissions.administrator or ctx.author.id == 636940258239447062:
        # Delete the specified amount of messages
        await ctx.channel.purge(limit=amount + 1)
        # Send a confirmation message
        await ctx.send(f'Deleted {amount} messages.', delete_after=5.0)

    else:
        # Send an error message if the user doesn't have the necessary permission
        await ctx.send('You are not authorised.', delete_after=5.0)


@bot.command()
async def peg(ctx):
    # Get the member object
    member = ctx.guild.get_member(user_id)
    
    # Get the role object
    role = ctx.guild.get_role(role_id)
    
    # Assign the role to the member
    await member.add_roles(role)
    
    # Send a confirmation message
    await ctx.send('Dhruva the maushi pegger fr')

# Create the "unpeg" command
@bot.command()
async def unpeg(ctx):
    # Get the user object
    if ctx.author.id == 345189736723251201:
        await ctx.send("Nice try dhruva")
    else:
        user = bot.get_user(user_id)
        
        # Get the member object
        member = ctx.guild.get_member(user_id)
        
        # Get the role object
        role = ctx.guild.get_role(role_id)
        
        # Remove the role from the member
        await member.remove_roles(role)
        
        # Send a confirmation message
        await ctx.send('Aw man')


# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. 
bot.run(TOKEN)