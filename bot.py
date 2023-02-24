import discord
import responses
import control
import re
import os
import log
import asyncio
import checkIn
import syncBot
import nest_asyncio
import interview

from datetime import datetime
from discord.utils import find
from discord.ext.commands import Bot
from enum import Enum

nest_asyncio.apply()

async def send_message(message, userMessage, is_private):
    try:
        response = responses.handle_response(userMessage)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)
    finally:
        pass

def run_discord_bot():
    
    TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
    intents = discord.Intents.all()
    client = discord.Client(intents=intents)
    botControl = control.Control()
    dateFormat = "%Y-%m-%d %H:%M:%S"
    dataDateFormat = "%Y-%m-%d"
    botSet = syncBot.SyncBot()
    checkControl = checkIn.CheckIn()

    @client.event
    async def process_users_message():
        printMsg = datetime.strftime(datetime.now(), dateFormat) + ": Bot start waiting " + str(botSet.waitTime) + ". "
        await asyncio.sleep(botSet.waitTime)
        users = checkControl.get_users()
        printMsg = printMsg + "End at " + datetime.strftime(datetime.now(), dateFormat) + ". "

        for guild in client.guilds:
            for channel in guild.text_channels:
                if channel.id in users.keys():
                    for key in users[channel.id].keys():
                        await channel.send(''.join(users[channel.id][key]))
        try:
            userDict = checkControl.check_to_db()
            if userDict:
                botControl.remove_checkIn(userDict)
                printMsg = printMsg + " Push to the DB!"
                log.write_into_log(printMsg)
        except Exception as e:
            await channel.send("No DB Connection!")
            printMsg = printMsg + " No DB Connection!"
            log.write_into_log(printMsg)
        finally:
            pass

        printMsg = ""
        # botSet.waitTime = 6
        botSet.waitTime = 24 * 60 * 60

    async def run_msg():
        await process_users_message()

    def start_task():
        while not botSet.botWait:
            botSet.botWait = 1
            task = asyncio.ensure_future(run_msg())
            task.add_done_callback(on_utilized)

    def on_utilized(_):
        botSet.botWait = 0
        start_task()

    @client.event
    async def on_ready():
        print(f'{client.user} is now running')
        printMsg = datetime.strftime(datetime.now(), dateFormat) + ": bot is now running"
        log.write_into_log(printMsg)
        hours = datetime.now().hour
        mins = datetime.now().minute
        botSet.waitTime = ((24-hours+6)*60 + (59-mins)) * 60
        # botSet.waitTime = 6
        # kick in the check in
        loop = asyncio.get_event_loop()
        try:
            start_task()
            loop.run_forever()
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()

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
        if 'check-in' in msgChannel:
            printMsg = datetime.strftime(datetime.now(), dateFormat) + ": " + userName  + " from channel " + msgChannel + " check-in."
            # print(f"Channel: {msgChannel} user: {userName} speak at the check-in.")
            checkControl.add_user(message.channel.id, userID, userName)
            log.write_into_log(printMsg)
        elif userMessage and userMessage[0] == '-':
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
            # this is for the mock interview
            elif '-interview' in userMessage:
                if 'mock-interview' in message.channel.name:
                    # get the question type
                    m = re.compile(r'-interview (bq|code)\s?(\w*)')
                    print(f"user massge is: {userMessage}")
                    try:
                        interViewType = m.match(userMessage)[1]
                        print(f"interview Type {interViewType}")
                        if interViewType.lower() == 'bq':
                            print(f"BQ questions {interViewType}")
                            newInterview = interview.Interview()
                            question = newInterview.get_bp_questions()
                            printMsg = datetime.strftime(datetime.now(), dateFormat) + ": " + userName  + " mock interview BQ: " + question
                            await send_message(message, question, is_private=False)
                        elif interViewType.lower() == 'code':
                            print(f"CODE questions {interViewType}")
                            try:
                                questionType = m.match(userMessage)[2]
                                question = botControl.get_linkCode_question(questionType)
                            except Exception as e:
                                question = botControl.get_linkCode_question('all')
                            finally:
                                pass
                            printMsg = datetime.strftime(datetime.now(), dateFormat) + ": " + userName  + " mock interview CODE ALL: " + question
                            await send_message(message, question, is_private=False)
                        else:
                            pass
                    except Exception as e:
                        printMsg = datetime.strftime(datetime.now(), dateFormat) + ": " + userName  + " mock interview NO TYPE: " + userMessage
                        await send_message(message, "Please specific your interview request (dp, code)?", is_private=True)
                    finally:
                        pass
                else:
                    await send_message(message, 'Please use the Mock Interview Voice channel for the interview mock', is_private=False)
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
                        # await send_message(message, userMessage, is_private=False)
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
            if 'Mock Interview' in str(after.channel.name):
                botControl.add_user(str(member.id))
                botControl.add_tag(member.id, "Mock Interview")
                await member.send("Start Timing for the Mock Interview!")
        else:
            if before.channel is not None:
                # print(f" {member.name} left the: {str(before.channel.name)} ")
                if 'Study Room' in str(before.channel.name) or 'Mock Interview' in str(before.channel.name):
                    if botControl.remove_user(str(member.id)):
                        await member.send("Finished Timing! (Use -get graph [Interval] [Chart Type] to see your data.)")
                    else:
                        await member.send("Error with the Timing! Please reach out for support!")

    client.run(TOKEN)

if __name__ == '__main__':
    pass
    # botModel = botModel.BotModel()