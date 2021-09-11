from db_connector import connector

def button(text, callback_data):
    return {'text': text, 'callback_data': callback_data}

def back_button(callback_data):
    return button('< назад', callback_data)

def main_menu_button():
    return button("Главное меню", "main_menu")

#creates rows of 1 button
def create_rows(iterable, prefix, back_callback = None, main_menu = False):
    result = [[button(iterable[i][1], f'{prefix}_{iterable[i][0]}')] 
              for i in range(0, len(iterable))]
    if back_callback:
        result.append([back_button(back_callback)])
    if main_menu:
        result.append([main_menu_button()])
    return result

#creates rows of 2 buttons
def create_rows_2(iterable, prefix, back_callback = None, main_menu = False):
    length = len(iterable)
    result = [[button(iterable[i][1], f'{prefix}_{iterable[i][0]}'),
               button(iterable[i+1][1],f'{prefix}_{iterable[i+1][0]}')] 
              for i in range(0, length - 1, 2)]
    if length % 2:
        result.append([button(iterable[-1][1], f'{prefix}_{iterable[-1][0]}')])
    if back_callback:
        result.append([back_button(back_callback)])
    if main_menu:
        result.append([main_menu_button()])
    return result

#creates rows of 3 buttons
def create_rows_3(iterable, prefix, back_callback = None, main_menu = False):
    length = len(iterable)
    result = [[button(iterable[i][1], f'{prefix}_{iterable[i][0]}'),
               button(iterable[i+1][1],f'{prefix}_{iterable[i+1][0]}'),
               button(iterable[i+2][1],f'{prefix}_{iterable[i+2][0]}')] 
              for i in range(0, length - 2, 3)]
    if length % 3 == 1:
        result.append([button(iterable[-1][1], f'{prefix}_{iterable[-1][0]}')])
    elif length % 3 == 2:
        result.append([button(iterable[-2][1], f'{prefix}_{iterable[-2][0]}'),
                       button(iterable[-1][1], f'{prefix}_{iterable[-1][0]}')])
    if back_callback:
        result.append([back_button(back_callback)])
    if main_menu:
        result.append([main_menu_button()])
    return result

def keyboard(text, rows):
    #кортеж, который будет распаковываться в edit_message как text и reply_markup
    return (text, {'inline_keyboard' : rows})


#------MAIN MENU------
#buttons
creatures_button = button('Существа', 'creatures_menu')
artifacts_button = button('Артефакты', 'artifacts_menu')
heroes_button = button('Герои', 'heroes_menu')
magic_button = button('Магия', 'magic_menu')
skills_button = button('Вторичные навыки', 'skills_menu')
#MAIN MENU KEYBOARD
main_menu = keyboard('Меню: ', [[creatures_button], [artifacts_button], 
                                [heroes_button], [magic_button], [skills_button]])


#-----CREATURES-----
#getting factions from db
factions = connector.execute("SELECT id, name FROM faction")
#creatures menu rows(3 buttons in a row)
creatures_menu_rows = create_rows_3(factions, "faction", "main_menu")
#CREATURES MENU KEYBOARD
creatures_menu = keyboard('Выберите фракцию: ', creatures_menu_rows)

#each faction's creatures
def faction_keyboards(factions_len):
    result = {}
    for i in range(factions_len):
        creatures = connector.execute(f"SELECT id, name FROM creature WHERE faction_id = {i+1}")
        if i == 11:
            kbrd = machines_keyboard(creatures)
        elif i == 10:
            kbrd = keyboard_with_2and3(creatures, (2, 7, 10))
        elif i == 9:
            kbrd = keyboard_with_2and3(creatures, (4,))
        else:
            kbrd = keyboard("Выберите существо: ", create_rows_2(creatures, "creature", "creatures_menu", main_menu=True))
        kbrd_dct = dict.fromkeys((f"faction_{i+1}",), kbrd)
        result.update(kbrd_dct)
    return result

def machines_keyboard(creatures):
    return keyboard("Выберите существо: ", create_rows(creatures, "creature", "creatures_menu", main_menu=True))

def keyboard_with_2and3(creatures, iterable):
    rows = []
    i = 0
    while i < len(creatures):
        if i in iterable:
            rows.extend(create_rows_3(creatures[i:i+3], "creature"))
            i += 3
        else:
            rows.extend(create_rows_2(creatures[i:i+2], "creature"))
            i += 2
    rows.append([back_button("creatures_menu")])
    rows.append([main_menu_button()])
    return keyboard('Выберите существо: ', rows)


#-----HEROES-----
#getting classes from db
classes = connector.execute("SELECT id, name FROM class")
#heroes menu rows(class names)
heroes_menu_rows = create_rows_2(classes, "class", "main_menu")
#HEROES MENU
heroes_menu = keyboard('Выберите класс: ', heroes_menu_rows)

#each class heroes
def classes_keyboards(classes_len):
    result = {}
    for c in range(classes_len):
        heroes = connector.execute(f"SELECT id, name FROM hero WHERE class = {c+1}")
        kbrd = keyboard("Выберите героя: ", create_rows_2(heroes, "hero", "heroes_menu", main_menu=True))
        kbrd_dict = dict.fromkeys((f'class_{c+1}',), kbrd)
        result.update(kbrd_dict)
    return result


#-----ARTIFACTS-----
by_category_button = button("По категории", "by_category_menu")
by_rarity_button = button("По редкости", "by_rarity_menu")
by_slot_button = button("По слоту в инвентаре", "by_slot_menu")
#ARTIFACTS MENU
artifacts_menu = keyboard("Группировка: ", [[by_category_button],
                                            [by_rarity_button],
                                            [by_slot_button],
                                            [back_button("main_menu")]])
#ARTIFACTS BY CATEGORY MENU
categories = connector.execute("SELECT id, name FROM category")
by_category_rows = create_rows_2(categories, "category", "artifacts_menu", main_menu=True)
by_category_menu = keyboard("Выберите категорию: ", by_category_rows)
#ARTIFACTS BY RARITY MENU
rarities = connector.execute("SELECT id, name FROM rarity")
by_rarity_rows = create_rows(rarities, "rarity", "artifacts_menu", main_menu=True)
by_rarity_menu = keyboard("Выберите редкость: ", by_rarity_rows)
#ARTIFACTS BY SLOT MENU
slots = connector.execute("SELECT id, name FROM slot")
by_slot_rows = create_rows_2(slots, "slot", "artifacts_menu", main_menu=True)
by_slot_menu = keyboard("Выберите слот: ", by_slot_rows)
#artifacts
def artifacts_keyboards(data_len, table_name, callback_data):
    result = {}
    for i in range(data_len):
        artifacts = connector.execute(f"SELECT id, name FROM artifact WHERE {table_name} = {i+1}")
        kbrd = keyboard("Выберите артефакт: ", create_rows_2(artifacts, "artifact", callback_data, main_menu=True))
        kbrd_dict = dict.fromkeys((f'{table_name}_{i+1}',), kbrd)
        result.update(kbrd_dict)
    return result


#-----SKILLS-----
skills = connector.execute("SELECT id, name FROM skill")
skills_rows = create_rows_3(skills, "skill", back_callback="main_menu")
skills_menu = keyboard("Выберите навык: ", skills_rows)


#-----MAGIC-----
def magic_menu(elements):
    rows = create_rows(elements, "element")
    inter_elemental = connector.execute("SELECT id, name FROM magic WHERE element IS NULL")
    rows.extend(create_rows_2(inter_elemental, "magic", back_callback="main_menu"))
    kbrd = keyboard("Выберите стихию: ", rows)
    return {"magic_menu": kbrd}

def elements_keyboards(elements):
    result = {}
    for e in elements:
        magic = connector.execute(f"SELECT id, name FROM magic WHERE element = {e}")
        kbrd = keyboard("Выберите заклинание: ", create_rows_2(magic, "magic", "magic_menu", main_menu=True))
        kbrd_dict = dict.fromkeys((f"element_{e}",), kbrd)
        result.update(kbrd_dict)
    return result


search_failed_keyboard = keyboard("Поиск не дал результатов, попробуйте другой запрос или воспользуйтесь Главным меню.",
                                    [[main_menu_button()]])

start_message_keyboard = keyboard("HOTABook - бот-справочник по игре Heroes of Might and Magic III: Horn of the Abbys.\
                                   \nВы можете воспользоваться интерактивным меню, чтобы найти необходимый игровой элемент, или поиском, написав боту название того, что хотите найти.\
                                   \nСкачать HOTA можно с официального сайта: https://h3hota.com/ru/download\
                                   \nДоступные команды:\
                                   \n/help, help, помощь, справка - вызов этого сообщения;\
                                   \n/menu, menu, main menu, меню, главное меню - вызов главного меню.",
                                    [[main_menu_button()]])

#Словарь со всеми клавиатурами
keyboards = {'main_menu': main_menu, 
             'creatures_menu': creatures_menu,
             **faction_keyboards(len(factions)),
             'heroes_menu': heroes_menu,
             **classes_keyboards(len(classes)),
             'artifacts_menu': artifacts_menu,
             'by_category_menu': by_category_menu,
             'by_rarity_menu': by_rarity_menu,
             'by_slot_menu': by_slot_menu,
             **artifacts_keyboards(len(categories), "category", "by_category_menu"),
             **artifacts_keyboards(len(rarities), "rarity", "by_rarity_menu"),
             **artifacts_keyboards(len(slots), "slot", "by_slot_menu"),
             'skills_menu': skills_menu,
             **magic_menu(skills[11:15]),
             **elements_keyboards(range(12,16)),
             'search_failed': search_failed_keyboard,
             'start_message': start_message_keyboard
            }
