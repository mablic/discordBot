import random

def handle_response(message):

    message = message.lower()
    if '-roll' in message:
        return str(random.randint(1,100))
    if '-hello' in message or '-hi' in message:
        return 'Sup?'
    if '-help' in message:
        response = "Help Menu..\nMessage bot with prefix '-'\n"
        response += "[-roll]: roll a dice from between 1 and 100\n"
        response += "[-help]: help menu\n"
        response += "[-private]: start a private chart with the bot\n"
        response += "[-get details]: get your records in details\n"
        response += "[-get graph]: [OPTIONAL(Interval)] [OPTIONAL(Graph type)] to graph your records\n"
        response += "      [OPTIONAL(Interval)]: [day](default) [week] [month] to group your data\n"
        response += "      [OPTIONAL(Graph type)]: [line](default) [bar] with the presentation of the data\n"
        response += "[-tag]: [OPTIONAL(Fous)] tag your focus to the clock\n"
        response += "      [OPTIONAL(Fous)]: your focus, please use the same moving forward"
        return response
    if '-private' in message:
        return 'Sup?'

    return message
        