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
        if message.content.startswith(":small_orange_diamond:"):
            pins = await message.channel.pins()
            if len(pins) > 0:
                for p in pins:
                    if p.content.startswith(":small_orange_diamond:"):
                        pin = p.content
                        pin = pin.split(' ')
                        msg = message.content
                        msg = msg.split(' ')
                        if msg[1] == pin[1]:
                            await p.unpin()
                        await message.pin()
            else:
                await message.pin()
        if message.content.startswith(":scroll:"):
            options = message.content
            options = options.split("\n")
            options = options[1:]
            for opt in options:
                temp = opt.replace('> ', '', 1)
                emoji = temp.split(' ')[0]
                await message.add_reaction(emoji)
            await message.pin()
    #Takes [!session] <SessionID> <Time> <AM/PM> <Timezone> <Month/Day> -> Logs a session with these arguments. \n [!session] <SessionID> status -> Outputs the  status of a session if it exists. \n [?session] <SessionID> -> Outputs the status of a session if it exists.
    if message.content.startswith('!session '):
        msg = message.content
        msg = msg.replace("!session ", '')
        if msg.find("status") >= 0:
            msg = msg.replace(" status", '')
            await message.channel.send(session.sessionQuery(msg, 1))
        else:
            await message.channel.send(session.session(msg))
    #Takes [?session] -> Outputs that session if it exists 
    if message.content.startswith('?session '):
        msg = message.content
        msg = msg.replace("?session ", '')
        await message.channel.send(session.sessionQuery(msg, 1))
    #Takes [!cleanup] -> Removes all expired sessions from the database (WIP)
    if message.content.startswith('!cleanup'):
        await message.channel.send(session.sessionListCleanup())
    #Takes [!allsessions] -> Outputs a list of all sessions.    
    if message.content.startswith('!sessions') or message.content.startswith('?sessions'):
        await message.channel.send(session.sessionQueryAll())
    #Takes [!removesession] <SessionID> -> Removes the SessionID given
    if message.content.startswith('!sessionrm '):
        msg = message.content
        msg = msg.replace("!sessionrm ", '')
        await message.channel.send(session.sessionRemove(msg))
    if message.content.startswith("!svote "):
        msg = message.content
        msg = msg.replace("!svote ", '')
        await message.channel.send(session.sessionVote(msg))
    if message.content.startswith("!evote"):
        pins = await message.channel.pins()
        if len(pins) > 0:
            for p in pins:
                if p.author == client.user:
                    if p.content.startswith(":scroll:"):
                        message_date = p.created_at
                        options = p.content
                        options = options.split("\n")
                        options = options[1:]
                        emoji_options = []
                        for o in range(len(options)):
                            options[o] = options[o].replace('> ', '', 1)
                            emoji_options.append(options[o].split(' ')[0])
                        mid = p.id
                        await p.unpin()
                        vote = await message.channel.fetch_message(mid)
                        x = 0
                        for reaction in vote.reactions:
                            if reaction.count > x:
                                x = reaction.count
                        winners = []
                        for reaction in vote.reactions:
                            if reaction.count == x:
                                winners.append(reaction.emoji)
                        tie = False
                        if len(winners) > 1:
                            reply = "**__Potential Options:__**\t:cat:\n"
                            tie = True
                        else:
                            reply = "**__The winner is:__**\t:trophy:\n"
                        winning_options = []
                        for win in winners:
                            for e in range(len(emoji_options)):
                                if str(win) == str(emoji_options[e]):
                                    reply += f"> {options[e]}\n"
                                    winning_options.append(options[e])
                        if tie == True:
                            reply += ":star2:**__Tie Breaker Vote!__**:star2:"
                            await message.channel.send(reply)
                            await message.channel.send(session.sessionVote(winning_options))
                        else:
                            await message.channel.send(reply)
    #Takes [!r | !roll] <#>d<Sides> +/- # +/- # ... -> Outputs rolls and total
    if message.content.startswith('!r ') or message.content.startswith("!roll "):
        msg = message.content
        if msg.find("!roll ") >= 0:
            msg = msg.replace("!roll ", '')
        elif msg.find("!r ") >= 0:
            msg = msg.replace("!r ", '')
        await message.channel.send(roll.roll(msg))

    if message.content.startswith("!help") or message.content.startswith("?help"):
        msg = message.content
        if msg.find("!help") >= 0:
            msg = msg.replace("!help", '')
        elif msg.find("?help") >= 0:
            msg = msg.replace("?help", '')
        if msg.find('sessions') >= 0:
            reply = "[?sessions | !sessions] -> Outputs a list of all available sessions in my Archives."
        elif msg.find('sessionrm') >= 0:
            reply = "[!sessionrm] <SessionID> -> Removes the session from my archives if it exists."
        elif msg.find('session') >= 0:
            reply = "[!session] <SessionID> <Time> <AM/PM> <Timezone> <Month/Day> -> Logs a session with these arguments. \n [!session] <SessionID> status -> Outputs the  status of a session if it exists. \n [?session] <SessionID> -> Outputs the status of a session if it exists."
        elif msg.find('cleanup') >= 0:
            reply = "[!cleanup] -> Removes all expired sessions from my Archives."
        elif (msg.find('r') >= 0 and len(msg) <= 4) or msg.find('roll') >= 0:
            reply = "[!r | !roll] <#>d<Sides> +/- # +/- # ... -> Outputs rolls and total | Optionally you can add "" with text inbetween to associate the roll with text."
        else:
            reply = "**__Commands:__** !session | ?session | ?sessions | !sessionrm | !cleanup | !r | !roll | !help | ?help \n> Help command will give detail for each of the commands if you append the command to the help command. Keep being awesome!"
        await message.channel.send(reply)

client.run(nethys)