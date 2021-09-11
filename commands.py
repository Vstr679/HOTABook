start_message_commands = ("/start", "/help", "help", "помощь", "справка")
main_menu_commands = ("/menu", "menu", "меню", "main menu", "главное меню")

commands = {
    'start_message': start_message_commands,
    'main_menu': main_menu_commands
}

def is_in_commands(message):
    for command in commands.items():
        if message in command[1]:
            return command[0]
    return None