import random

def handle_response(message, check):

    message = message.lower()
    if '-roll' in message:
        return str(random.randint(1,100))
    if '-hello' in message or '-hi' in message:
        return 'Sup?'
    if '-help' in message:
        response = "***Help Menu***\n***Message bot with prefix '-'***\n***Visit our WEBSITE for Details***\n\n"
        response += "> https://studygrouppal.com/   \n"
        response += "> **The Bot will automatically record your studying time when you enter any voice channel with (Study Room) in the name.**\n"
        response += "> **Find your study records in graph from our website. It's free!**\n\n"
        response += "***GENERAL***\n\n"
        response += "> **-help**: help menu\n"
        response += "> **-private**: start a private chart with the bot\n\n"
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
        response += "***PRIVATE MESSAGE WITH THE BOT ONLY***\n\n"
        response += "> **-tag (fous)**: tag your focus to the clock\n"
        response += "> \t__optional(fous)__: your focus, please use the same moving forward\n"
        response += "> \t__For example__: -tag Math: the bot will record the time as Math."
        return response
    if '-private' in message:
        return 'Sup?'
    if not check and '-' in message:
        return "I don't understand this, please use -help for more info."

    return message
        