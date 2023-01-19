import discord
import responses
import control
import re
import os
import log

from datetime import datetime
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
    dateFormat = "%Y-%m-%d %H:%M:%S"
    dataDateFormat = "%Y-%m-%d"

    @client.event
    async def on_ready():
        print(f'{client.user} is now running')
        printMsg = datetime.strftime(datetime.now(), dateFormat) + ": bot is now running"
        log.write_into_log(printMsg)
    
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
        printMsg = ""
        if userMessage and userMessage[0] == '-':
            if '-get date' in userMessage:
                m = re.compile(r'(-get date)\s?([0-9]{4}-[0-9]{2}-[0-9]{2})')
                if not m.match(userMessage):
                    day = datetime.strftime(datetime.now(), dataDateFormat)
                else:
                    m = m.match(userMessage)
                    day = m[2]
                printMsg = datetime.strftime(datetime.now(), dateFormat) + ": " + userName  + " from channel " + msgChannel + " get date: " + day
                # print(printMsg)
                try:
                    filePath = botControl.get_data_graph(userID, 'pie', 'day', day)
                    with open(filePath, 'rb') as f:
                        picture = discord.File(f)
                        await message.channel.send(file=picture)
                    botControl.remove_file(filePath)
                except ValueError as e:
                    await send_message(message, "No DB Connection!", is_private=True)
                    printMsg = printMsg + " No DB Connection!"
                except Exception as e:
                    await send_message(message, "No Data Found!", is_private=True)
                    printMsg = printMsg + " No Data Found!"
                finally:
                    pass
            elif message.channel.id == dmChannel.id:
                if '-tag' in userMessage:
                    try:
                        m = re.compile(r'(-tag)\s?(.*)')
                        tagName = m.match(userMessage)
                        tagName = tagName[2].upper()
                        # print(f"PRIVATE: {userName} add tag '{tagName}'")
                        printMsg = datetime.strftime(datetime.now(), dateFormat) + ": " + userName  + " add tag: " + tagName
                        botControl.add_tag(userID, tagName) 
                    except Exception as e:
                        print(e)
                        printMsg = datetime.strftime(datetime.now(), dateFormat) + ": " + userName  + " running into error: " + str(e)
                    finally:
                        pass
                elif '-get details' in userMessage:
                    try:
                        response = botControl.get_data_details(userID)
                        printMsg = datetime.strftime(datetime.now(), dateFormat) + ": " + userName  + " get details: " + userMessage
                        await send_message(message, 'details in minutes by date below...', is_private=True)
                        for r in response:
                            await send_message(message, r, is_private=True)
                    except Exception as e:
                        await send_message(message, "No DB Connection!", is_private=True)
                        printMsg = printMsg + " No DB Connection!"
                    finally:
                        pass
                elif '-get graph' in userMessage:
                    # print(f"GET GRAPH: {userName} said '{userMessage}'")
                    try:
                        m = re.compile(r'(-get graph)\s?([a-zA-Z]*)\s?([a-zA-Z]*)')
                        m = m.match(userMessage)
                        interval = 'day' if m[2] == '' else m[2]
                        chartType = 'line' if m[3] == '' else m[3]
                        # print(f"INTERVAL: {interval} CHARTTYPE '{chartType}')")
                        printMsg = datetime.strftime(datetime.now(), dateFormat) + ": " + userName  + " get graph: (interval: " + str(interval) + ") (chartType: " + chartType + ")" 
                        try:
                            filePath = botControl.get_data_graph(userID, chartType, interval, '')
                            with open(filePath, 'rb') as f:
                                picture = discord.File(f)
                                await message.channel.send(file=picture)
                            botControl.remove_file(filePath)
                        except ValueError as e:
                            await send_message(message, "No DB Connection!", is_private=True)
                            printMsg = printMsg + " No DB Connection!"
                        except Exception as e:
                            await send_message(message, "No Data Found!", is_private=True)
                            printMsg = printMsg + " No Data Found!"
                        finally:
                            pass
                    except Exception as e:
                        print(e)
                        printMsg = datetime.strftime(datetime.now(), dateFormat) + ": " + userName  + " get graph: (interval: " + str(interval) + ") (chartType: " + chartType + ") error: " + str(e) 
                    finally:
                        pass
                else:
                    if userMessage and userMessage[0] == '-':
                        printMsg = datetime.strftime(datetime.now(), dateFormat) + ": " + userName  + " send message: " + userMessage
                        await send_message(message, userMessage, is_private=False)
            else:
                # print(f"PRIVATE: {userName} said '{userMessage}' ({msgChannel})")
                if '-private' in userMessage:
                        printMsg = datetime.strftime(datetime.now(), dateFormat) + ": " + userName  + " from channel " + msgChannel + " send message for private: " + userMessage
                        await send_message(message, userMessage, is_private=True)
                else:
                    printMsg = datetime.strftime(datetime.now(), dateFormat) + ": " + userName  + " from channel " + msgChannel + " send message for public: " + userMessage
                    await send_message(message, userMessage, is_private=False)
            log.write_into_log(printMsg)

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
                    if botControl.remove_user(str(member.id)):
                        await member.send("Finished Timing! (Use -get graph [Interval] [Chart Type] to see your data.)")
                    else:
                        await member.send("Error with the Timing! Please reach out for support!")

    client.run(TOKEN)

if __name__ == '__main__':
    pass
    # botModel = botModel.BotModel()