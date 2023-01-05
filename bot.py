import discord
import responses
import control
import re
import os

from discord.utils import find
from discord.ext.commands import Bot

async def send_message(message, userMessage, is_private):
    try:
        response = responses.handle_response(userMessage)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


def run_discord_bot():
    TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
    intents = discord.Intents.all()
    # intents.members = True
    client = discord.Client(intents=intents)
    botControl = control.Control()

    @client.event
    async def on_ready():
        print(f'{client.user} is now running')
    
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        
        userName = str(message.author)
        userMessage = str(message.content)
        msgChannel = str(message.channel)
        userID = str(message.author.id)
        dmChannel = await message.author.create_dm()

        # print(f"{userName} said '{userMessage}' ({msgChannel})")

        if message.channel.id == dmChannel.id:
            if '-tag' in userMessage:
                try:
                    m = re.compile(r'(-tag)\s?(.*)')
                    tagName = m.match(userMessage)
                    tagName = tagName[2].upper()
                    # print(f"PRIVATE: {userName} add tag '{tagName}'")
                    botControl.add_tag(userID, tagName) 
                except Exception as e:
                    print(e)
                finally:
                    pass
            elif '-get details' in userMessage:
                response = botControl.get_data_details(userID)
                # print(f"DETAILS: {response} add message '{userMessage}'")
                await send_message(message, 'details in minutes by date below...', is_private=True)
                for r in response:
                    await send_message(message, r, is_private=True)
            elif '-get graph' in userMessage:
                # print(f"GET GRAPH: {userName} said '{userMessage}'")
                try:
                    m = re.compile(r'(-get graph)\s?([a-zA-Z]*)\s?([a-zA-Z]*)')
                    m = m.match(userMessage)
                    interval = 'day' if m[2] == '' else m[2]
                    chartType = 'line' if m[3] == '' else m[3]
                    # print(f"INTERVAL: {interval} CHARTTYPE '{chartType}')")
                    filePath = botControl.get_data_graph(userID, interval, chartType)
                    with open(filePath, 'rb') as f:
                        picture = discord.File(f)
                        await message.channel.send(file=picture)
                    botControl.remove_file(filePath)
                except Exception as e:
                    print(e)
                finally:
                    pass
            else:
                if userMessage and userMessage[0] == '-':
                    if '-private' in userMessage:
                        await send_message(message, userMessage, is_private=True)
                    else:
                        await send_message(message, userMessage, is_private=False)
        else:
            # print(f"PRIVATE: {userName} said '{userMessage}' ({msgChannel})")
            if userMessage and userMessage[0] == '-':
                if '-private' in userMessage:
                    await send_message(message, userMessage, is_private=True)
                else:
                    await send_message(message, userMessage, is_private=False)

    @client.event
    async def on_voice_state_update(member, before, after):
        if after.channel is not None:
            if before.channel is not None and 'Study Room' in str(before.channel.name):
                # print(f" {member.name} left the: {str(before.channel.name)} and join the: {str(after.channel.name)} ")
                return
            
            if 'Study Room' in str(after.channel.name):
                # print(f" {member.name} join the: {str(after.channel.name)} ")
                botControl.add_user(str(member.id))
                await member.send("Start Timing! (Use -tag [XX your Tag] to add your focus.)")
        else:
            if before.channel is not None:
                # print(f" {member.name} left the: {str(before.channel.name)} ")
                if 'Study Room' in str(before.channel.name):
                    botControl.remove_user(str(member.id))
                    await member.send("Finished Timing! (Use -get graph [Interval] [Chart Type] to see your data.)")

    client.run(TOKEN)

if __name__ == '__main__':

    pass
    # botModel = botModel.BotModel()