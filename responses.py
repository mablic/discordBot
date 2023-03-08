import random

def handle_response(message):

    message = message.lower()
    if '-roll' in message:
        return str(random.randint(1,100))
    if '-hello' in message or '-hi' in message:
        return 'Sup?'
    if '-help' in message:
        response +="-----------------------------------------Controls-----------------------------------------\n\n"
        response += "Help Menu..\nMessage bot with prefix '-'\n\n"
        response += "-roll: roll a dice from between 1 and 100\n"
        response += "-help: help menu\n"
        response += "-scheduler REQUIRED(1-24) OPTIONAL(Message): schedule a reminder with the bot in the scheduler text channel\n"
        response += "   REQUIRED(1-24): send the reminder at the hours (24 format in CST)\n"
        response += "   OPTIONAL(Type): custom message if any, otherwise:妈妈喊你打卡啦！\n"
        response += "-interview REQUIRED(bq/code) OPTIONAL(Type): generate a random interview question in the mock-interview text channel\n"
        response += "   REQUIRED(bq/code)\n"
        response += "       bq:     behavior questions\n"
        response += "       code:   leetcode questions\n"
        response += "   OPTIONAL(Type)\n"
        response += "       easy:   easy leetcode questions\n"
        response += "       medium: medium leetcode questions\n"
        response += "       hard:   hard leetcode questions\n"
        response += "   Exampe: -interview code easy\n"
        response += "-private: start a private chart with the bot\n"
        response += "-get day OPTIONAL(date): get the pie chart of the date\n\n"
        response += "-----------------------------------PRIVATE CHANNEL ONLY-----------------------------------\n\n"
        response += "-get details: get your records in details\n"
        response += "-get graph OPTIONAL(Interval) OPTIONAL(Graph type) to graph your records\n"
        response += "   OPTIONAL(Interval): [day](default) [week] [month] to group your data\n"
        response += "   OPTIONAL(Graph type): [line](default) [bar] with the presentation of the data\n"
        response += "   Exampe: -get graph day bar\n"
        response += "-tag OPTIONAL(Fous) tag your focus to the clock\n"
        response += "   OPTIONAL(Fous): your focus, please use the same moving forward\n\n"
        response += "------------------------------------------WEBSITE---------------------------------------------\n\n"
        response += "To the LeetCode Challengers, you can now use below website on your journey \n"
        response += "https://sdashboard.herokuapp.com/   \n"
        response += "Future release with the control on this StudyBot in the website to come\n\n"
        return response
    if '-private' in message:
        return 'Sup?'

    return message
        