# NETHYS

import os
import random
import discord
#import ntplib
import time
from dotenv import load_dotenv
from discord.ext import commands, tasks
from datetime import timedelta, date
from datetime import datetime, timezone
import asyncio
import datetime

#Nethys Modules \/
import roll
import session

load_dotenv()

nethys = os.getenv('NETHYS_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        pins = await message.channel.pins()
        if message.content.startswith(":small_orange_diamond:"):
            for p in pins:
                print('\nPins: ',p.id)
                print('Content: ',p.content)
                if p.content.startswith(":small_orange_diamond:"):
                    pin = p.content
                    pin = pin.split(' ')
                    msg = message.content
                    msg = msg.split(' ')
                    if msg[1] == pin[1]:
                        await p.unpin()
                    await message.pin()
        return
    #Takes [!session] <SessionID> <Time> <AM/PM> <Timezone> <Month/Day> -> Logs a session with these arguments. \n [!session] <SessionID> status -> Outputs the  status of a session if it exists. \n [?session] <SessionID> -> Outputs the status of a session if it exists.
    if message.content.startswith('!session'):
        msg = message.content
        msg = msg.replace("!session ", '')
        if msg.find("status") >= 0:
            msg = msg.replace(" status", '')
            await message.channel.send(session.sessionQuery(msg))
        else:
            await message.channel.send(session.session(msg))
    #Takes [?session] -> Outputs that session if it exists 
    if message.content.startswith('?session'):
        msg = message.content
        msg = msg.replace("?session ", '')
        await message.channel.send(session.sessionQuery(msg))
    #Takes [!cleanup] -> Removes all expired sessions from the database (WIP)
    if message.content.startswith('!cleanup'):
        await message.channel.send(session.sessionListCleanup())
    #Takes [!allsessions] -> Outputs a list of all sessions.    
    if message.content.startswith('!allsessions'):
        await message.channel.send(session.sessionQueryAll())
    #Takes [!removesession] <SessionID> -> Removes the SessionID given
    if message.content.startswith('!removesession'):
        msg = message.content
        msg = msg.replace("!removesession ", '')
        await message.channel.send(session.sessionRemove(msg))
    if message.content.startswith("!svote"):
        msg = message.content
        msg = msg.replace("!svote ", '')
        client.get_emoji
        await message.channel.send(session.sessionVote(msg))
    #Takes [!r | !roll] <#>d<Sides> +/- # +/- # ... -> Outputs rolls and total
    if message.content.startswith('!r '):
        msg = message.content
        if msg.find("!roll ") >= 0:
            msg = msg.replace("!roll ", '')
        elif msg.find("!r ") >= 0:
            msg = msg.replace("!r ", '')
        else:
            msg = "Incorrect syntax, expected: #d# <+ or -> # | Optionally you can add "" with text inbetween to associate the roll with text."
        await message.channel.send(roll.roll(msg))

    if message.content.startswith("!help") or message.content.startswith("?help"):
        msg = message.content
        if msg.find("!help") >= 0:
            msg = msg.replace("!help", '')
        elif msg.find("?help") >= 0:
            msg = msg.replace("?help", '')
        if msg.find('session') >= 0:
            reply = "[!session] <SessionID> <Time> <AM/PM> <Timezone> <Month/Day> -> Logs a session with these arguments. \n [!session] <SessionID> status -> Outputs the  status of a session if it exists. \n [?session] <SessionID> -> Outputs the status of a session if it exists."
        elif msg.find('cleanup') >= 0:
            reply = "[!cleanup] -> Removes all expired sessions from my Archives."
        elif msg.find('allsessions') >= 0:
            reply = "[!allsessions] -> Outputs a list of all available sessions in my Archives."
        elif msg.find('removesession') >= 0:
            reply = "[!removesession] <SessionID> -> Removes the session from my archives if it exists."
        elif (msg.find('r') >= 0 and len(msg) <= 4) or msg.find('roll') >= 0:
            reply = "[!r | !roll] <#>d<Sides> +/- # +/- # ... -> Outputs rolls and total | Optionally you can add "" with text inbetween to associate the roll with text."
        else:
            reply = "Commands: !session | ?session | !cleanup | !allsessions | !removesession | !r | !roll | !help | ?help | Help command will give detail for each of the commands if you append the command to the help command. Keep being awesome!"
        await message.channel.send(reply)

client.run(nethys)