import random

def handle_response(message):

    if message == '-roll':
        return str(random.randint(1,6))
    
    if message == '-help':
        return "Help Menu.."
    
    return message
        