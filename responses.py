import random

def handle_response(message, check):

    message = message.lower()
    if '-roll' in message:
        return str(random.randint(1,100))
    if '-hello' in message or '-hi' in message:
        return 'Sup?'
    if '-help' in message:
        response = "***Help Menu***\n***Message bot with prefix*** '-'\n\n"
        response += "> **-roll**: roll a dice from between 1 and 100\n"
        response += "> **-help**: help menu\n"
        response += "> **-private**: start a private chart with the bot\n"
        response += "> **-get day (date)**: get the pie chart of the date in YYYY-MM-dd\n\n"
        response += "***SCHEDULER TEXT CHANNEL ONLY***\n\n"
        response += "> **-scheduler (1-23) (Message)**:\n"
        response += "> \t__required(1-23)__: send the reminder at the hours (24 format in CST)\n"
        response += "> \t__optional(type)__: custom message if any, otherwise:妈妈喊你打卡啦！\n\n"
        response += "***MOCK INTERVIEW TEXT CHANNEL ONLY***\n\n"
        response += "> **-interview (bq/code) (type)**:\n"
        response += "> \t__required(bq/code)__\n"
        response += "> \t\tbq: behavior questions\n"
        response += "> \t\tcode: leetcode questions\n"
        response += "> \t__optional (type)__\n"
        response += "> \t\teasy: easy leetcode questions\n"
        response += "> \t\tmedium: medium leetcode questions\n"
        response += "> \t\thard: hard leetcode questions\n"
        response += "> \t**exampe: -interview code easy**\n\n"
        response += "***PRIVATE CHANNEL ONLY***\n\n"
        response += "> **-get details**: get your records in details\n"
        response += "> **-get graph (interval) (graph type)**: graph your records\n"
        response += "> \t__optional(interval)__: \n"
        response += "> \t\tday: default \n"
        response += "> \t\tweek\n"
        response += "> \t\tmonth\n"
        response += "> \t__optional(graph type)__:\n"
        response += "> \t\tline: default \n"
        response += "> \t\tbar\n"
        response += "> \t**exampe: -get graph day bar**\n"
        response += "> **-tag (fous)**: tag your focus to the clock\n"
        response += "> \t__optional(fous)__: your focus, please use the same moving forward\n\n"
        response += "***WEBSITE***\n\n"
        response += "> https://sdashboard.herokuapp.com/   \n"
        return response
    if '-private' in message:
        return 'Sup?'
    if not check and '-' in message:
        return "I don't understand this, please use -help for more info."

    return message
        