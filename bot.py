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

from datetime import datetime, timedelta
from discord.utils import find
from discord.ext.commands import Bot
from enum import Enum

nest_asyncio.apply()

async def send_message(message, userMessage, is_private, check=True):
    try:
        response = responses.handle_response(userMessage, check)
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
        botSet.botHourWait += 1
        printMsg = datetime.strftime(datetime.now(), dateFormat) + ": Bot start waiting " + str(botSet.waitTime) + ". "
        await asyncio.sleep(botSet.waitTime)
        try:
            timeZoneUsers = botControl.get_time_zone_users()
            users = checkControl.get_users()
        except Exception as e:
            printMsg + ' ' + e
            log.write_into_log(printMsg)
            return
        
        printMsg = printMsg + "End at " + datetime.strftime(datetime.now(), dateFormat) + ". "
        removeUsers = []
        if users:
            for userId in users.keys():
                for guildId in users[userId].keys():
                    if datetime.strftime(datetime.now(), "%H") == '00':
                        # central time msg
                        if userId not in timeZoneUsers or int(timeZoneUsers[userId]) == int(0):
                            removeUsers.append(users[userId][guildId])
                    if userId in timeZoneUsers:
                        timeZone = timeZoneUsers[userId]['timeZone']
                        if datetime.strftime(datetime.now() + timedelta(hours=int(timeZone)), '%H') == '00':
                            removeUsers.append(users[userId][guildId])
        if removeUsers:
            for user in removeUsers:
                guildId = int(user['guildId'])
                channelId = int(user['channelId'])
                userId = user['userId']
                guild = client.get_guild(int(guildId))
                channel = guild.get_channel(channelId)
                if channel:
                    await channel.send(user['details'])
                    timeZone = 0
                    if userId in timeZoneUsers:
                        timeZone = timeZoneUsers[userId]['timeZone']
                    try:
                        checkData = checkControl.check_to_db(userId, datetime.now() + timedelta(hours=int(timeZone)))
                        botControl.add_checkIn(checkData)
                    except Exception as e:
                        await channel.send("No DB Connection to Check-In!")
                        printMsg = printMsg + " No DB Connection!"
                        log.write_into_log(printMsg)
                    finally:
                        pass
        printMsg = ""
        # botSet.waitTime = 10
        botSet.waitTime = 60 * 60

    @client.event
    async def scheduler_users_message():
        botSet.botHourWait += 1
        printMsg = datetime.strftime(datetime.now(), dateFormat) + ": Bot start scheduler " + str(botSet.notifyTime) + ". "
        await asyncio.sleep(botSet.notifyTime)
        schedulerUsers = botControl.get_notification()
        timeZoneUsers = botControl.get_time_zone_users()
        users = checkControl.get_users()
        printMsg = printMsg + "End at " + datetime.strftime(datetime.now(), dateFormat) + ". "

        checkInUser = {}
        if users:
            for userId in users.keys():
                for guildId in users[userId].keys():
                    # currUser = users[userId][guildId]['userName']
                    if guildId not in checkInUser.keys():
                        checkInUser[guildId] = set()
                    currUser = users[userId][guildId]['userName']
                    checkInUser[guildId].add(currUser)
        for guild in client.guilds:
            for channel in guild.text_channels:
                # if str(channel.id) != '1082853330369396817':
                #     continue
                reminderDict = {}
                if str(channel.id) in schedulerUsers.keys():
                    for nTime in schedulerUsers[str(channel.id)].keys():
                        for itm in schedulerUsers[str(channel.id)][nTime]:
                            user, userMsg, userId = itm
                            timeZone = 0
                            if str(userId) in timeZoneUsers.keys():
                                timeZone = timeZoneUsers[str(userId)]['timeZone']
                            currentHour = datetime.strftime(datetime.now() + timedelta(hours=int(timeZone)),"%H")
                            if int(nTime) <= int(currentHour):
                                if str(guild.id) not in checkInUser.keys():
                                    reminderDict[user] = userMsg
                                else:
                                    if user not in checkInUser[str(guild.id)]:
                                        reminderDict[user] = userMsg
                for userName in reminderDict.keys():
                    member = discord.utils.get(guild.members, name=userName[:userName.find('#')])
                    if member is not None:
                        await channel.send(f"{member.mention} , {reminderDict[userName]}!")
                        printMsg += 'send message to ' + userName[:userName.find('#')]
                    else:
                        printMsg += userName[:userName.find('#')] + ' NOT FOUND!'
                    log.write_into_log(printMsg)
        printMsg = ""
        # botSet.notifyTime = 10
        botSet.notifyTime = 60 * 60

    async def start_task():
        # print(f"Start Mutli-Tasks")
        while not botSet.stop_bot():
            task1 = asyncio.ensure_future(process_users_message())
            task2 = asyncio.ensure_future(scheduler_users_message())
            task1.add_done_callback(on_utilized)
            task2.add_done_callback(on_utilized)
            await asyncio.gather(task1, task2)

    def on_utilized(_):
        botSet.botHourWait -= 1

    @client.event
    async def on_ready():
        print(f'{client.user} is now running')
        printMsg = datetime.strftime(datetime.now(), dateFormat) + ": bot is now running"
        log.write_into_log(printMsg)
        hours = datetime.now().hour
        mins = datetime.now().minute
        botSet.waitTime = (59-mins) * 60
        botSet.notifyTime = (59-mins) * 60
        botSet.checkRun = 2
        # botSet.waitTime = 10
        # botSet.notifyTime = 10
        # kick in the check in
        loop = asyncio.get_event_loop()
        try:
            # start_task()
            asyncio.run(start_task())
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
        guild = message.guild

        # print(f"{userName} said '{userMessage}' ({msgChannel})")
        printMsg = ""
        if 'check-in' in msgChannel:
            printMsg = datetime.strftime(datetime.now(), dateFormat) + ": " + userName  + " from channel " + msgChannel + " check-in."
            checkControl.add_user(guild.id, message.channel.id, userID, userName)
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
                    # print(f"user massge is: {userMessage}")
                    try:
                        interViewType = m.match(userMessage)[1]
                        # print(f"interview Type {interViewType}")
                        if interViewType.lower() == 'bq':
                            # print(f"BQ questions {interViewType}")
                            newInterview = interview.Interview()
                            question = newInterview.get_bp_questions()
                            printMsg = datetime.strftime(datetime.now(), dateFormat) + ": " + userName  + " mock interview BQ: " + question
                            await send_message(message, question, is_private=False)
                        elif interViewType.lower() == 'code':
                            # print(f"CODE questions {interViewType}")
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
                        await send_message(message, "Please specific your interview request (bq, code)?", is_private=False)
                    finally:
                        pass
                else:
                    await send_message(message, 'Please use the Mock Interview Voice channel for the interview mock', is_private=False)
            # set the scheduler
            elif '-scheduler' in userMessage and 'scheduler' in message.channel.name:
                # remove scheduler
                msgDict = {}
                msgDict['userId'] = userID
                msgDict['userName'] = str(userName)
                msgDict['channelName'] = str(message.channel.name)
                msgDict['channelId'] = str(message.channel.id)
                if 'remove' in userMessage:
                    botControl.remove_notification(msgDict)
                    printMsg = datetime.strftime(datetime.now(), dateFormat) + ": Scheduler " + userName  + " Channel: " + message.channel.name + " REMOVED. Mssage:" + userMessage
                    await send_message(message, "Successfully removed from the scheduler.", is_private=True)
                else:
                    m = re.compile(r'(-scheduler)\s?(2[0-3]|[0-1]?[0-9])\s?(.*)')
                    try:
                        scheduler = m.match(userMessage)
                        msgDict['time'] = str(scheduler[2])
                        msgDict['message'] = str(scheduler[3])
                        printMsg = datetime.strftime(datetime.now(), dateFormat) + ": Scheduler " + userName  + " Channel: " + message.channel.name + " ADD. Mssage:" + userMessage
                        botControl.add_notification(msgDict)
                        await send_message(message, 'Scheduler for ' + str(msgDict['time']) + ' with the notification: ' + str(msgDict['message']), is_private=True)
                    except Exception as e:
                        printMsg = datetime.strftime(datetime.now(), dateFormat) + ": Scheduler " + userName  + " Channel: " + message.channel.name + " FAIL. Mssage:" + userMessage
                        await send_message(message, "Not able to schedule, please make sure using -schedule XX XXXX", is_private=True)
                    finally:
                        pass
            # direct message ONLY
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
                elif '-timezone' in userMessage:
                    userDict = {}
                    userDict['userId'] = userID
                    userDict['userName'] = userName
                    if '-remove' in userMessage:
                        try:
                            botControl.remove_time_zone(userDict)
                            await send_message(message, "Successfully remove TimeZone information.", is_private=True)
                        except Exception as e:
                            await send_message(message, "Unable to remove TimeZone information.", is_private=True)
                            printMsg = printMsg + " Unable to remove TimeZone for user" + userDict['userName']
                        finally:
                            pass
                    else:
                        try:
                            m = re.compile(r'(-timezone)\s?(\-[0-6]|\+?20|\+?1[1-9]|\+?[0-9])')
                            m = m.match(userMessage)
                            timeDiff = m[2]
                            userDict['timeZone'] = timeDiff
                            botControl.add_time_zone(userDict)
                            await send_message(message, "Submit TimeZone information " + userDict['timeZone'] + '.', is_private=True)
                        except Exception as e:
                            await send_message(message, "Unable to submit TimeZone information.", is_private=True)
                            printMsg = printMsg + " No Data Found!"                       
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
                    await send_message(message, userMessage, is_private=False, check=False)
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
                botControl.add_tag(str(member.id), "Mock Interview")
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