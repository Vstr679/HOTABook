from db_connector import connector
from keyboards import keyboard, button, back_button, main_menu_button

class SearchClass(object):

    def __init__(self):
        self.tables_to_search = ["creature", "artifact", "hero", "magic", "skill"]

    def _handle_callback(self, callback):
        self.table_name = callback.split("_")[0]
        self.attribute = callback.split("_")[1]

    def _return_image_and_keyboard(self, img, text, back_button_callback):
        image_path = "./images/" + img
        image_file = open(image_path, 'rb')
        if not back_button_callback:
            kbrd = keyboard(text, [[main_menu_button()]])
        elif back_button_callback == "search_results":
            kbrd = keyboard(text, [[back_button("search_results")], [main_menu_button()]])
        else:
            kbrd = keyboard(text, [[back_button(back_button_callback)], [main_menu_button()]])
        return (image_file, kbrd)

    def _get_creature(self, back_button_callback):
        data = connector.execute(f"SELECT creature.id, creature.name, img, level, faction.name, min_damage, max_damage, attack, \
                                          defense, health, speed, growth, price, resource, special, ai_value \
                                   FROM creature, faction \
                                   WHERE creature.id = '{self.attribute}' and creature.faction_id = faction.id")
        return self._handle_creature(data[0], back_button_callback)

    def _handle_creature(self, creature, back_button_callback):
        text = f'{creature[1]}\
        \n__________ \
        \nФракция: {creature[4]}\
        \n__________ \
        \nУровень: {creature[3]}\
        \n__________ \
        \nМинимальный урон: {creature[5]}\
        \n__________ \
        \nМаксимальный урон: {creature[6]}\
        \n__________ \
        \nАтака: {creature[7]}\
        \n__________ \
        \nЗащита: {creature[8]}\
        \n__________ \
        \nЗдоровье: {creature[9]}\
        \n__________ \
        \nСкорость: {creature[10]}\
        \n__________ \
        \nПрирост: {creature[11]}\
        \n__________ \
        \nЦена: {creature[12]}\
        \n__________ \
        \nРесурс: {creature[13] if creature[13] else "не требуется"}\
        \n__________ \
        \nСпособности: {creature[14] if creature[14] else "нет"}\
        \n__________ \
        \nAI value: {creature[15]}'
        return self._return_image_and_keyboard(str(creature[2]), text, back_button_callback)

    def _get_artifact(self, back_button_callback):
        data = connector.execute(f"SELECT artifact.id, artifact.name, price, slot.name, rarity.name, category.name, description, img \
                                   FROM artifact, slot, rarity, category \
                                   WHERE artifact.id = '{self.attribute}' and artifact.slot = slot.id \
                                         and artifact.rarity = rarity.id and artifact.category = category.id")
        return self._handle_artifact(data[0], back_button_callback)

    def _handle_artifact(self, artifact, back_button_callback):
        text = f'{artifact[1]}\
        \n__________ \
        \nЦена: {artifact[2]}\
        \n__________ \
        \nСлот: {artifact[3]}\
        \n__________ \
        \nРедкость: {artifact[4]}\
        \n__________ \
        \nКатегория: {artifact[5]}\
        \n__________ \
        \nОписание: {artifact[6]}'
        return self._return_image_and_keyboard(str(artifact[7]), text, back_button_callback)

    def _get_hero(self, back_button_callback):
        data = connector.execute(f"SELECT hero.id, hero.name, class.name, specialization.name, specialization.description, magic.name, skill1.name, skill2.name, moves, \
                                          unit_1_min, unit_1_max, creature1.name, unit_2_min, unit_2_max, creature2.name, unit_3_min, unit_3_max, creature3.name, hero.img \
                                   FROM hero \
                                   JOIN class ON hero.class = class.id \
                                   JOIN specialization ON hero.specialization = specialization.id \
                                   LEFT OUTER JOIN magic ON hero.magic = magic.id \
                                   LEFT OUTER JOIN skill as skill1 ON hero.skill_1 = skill1.id \
                                   LEFT OUTER JOIN skill as skill2 ON hero.skill_2 = skill2.id \
                                   JOIN creature as creature1 ON hero.unit_1 = creature1.id \
                                   JOIN creature as creature2 ON hero.unit_2 = creature2.id \
                                   JOIN creature as creature3 ON hero.unit_3 = creature3.id \
                                   WHERE hero.id = '{self.attribute}'")
        return self._handle_hero(data[0], back_button_callback)

    def _handle_hero(self, hero, back_button_callback):
        text = f'{hero[1]}\
        \n__________ \
        \nКласс: {hero[2]}\
        \n__________ \
        \nСпециализация: {hero[3]}. {hero[4]}\
        \n__________ \
        \nЗаклинание: {hero[5] if hero[5] else "нет"}\
        \n__________ \
        \nСпособность 1: {hero[6]}\
        \n__________ \
        \nСпособность 2: {hero[7] if hero[7] else "нет"}\
        \n__________ \
        \nОчки передвижения: {hero[8]}\
        \n__________ \
        \nЮниты:\
        \n{hero[11]} {hero[9]} - {hero[10]}\
        \n{hero[14]} {hero[12]} - {hero[13]}\
        \n{hero[17]} {hero[15]} - {hero[16]}'
        return self._return_image_and_keyboard(str(hero[18]), text, back_button_callback)

    def _get_magic(self, back_button_callback):
        data = connector.execute(f"SELECT magic.id, magic.name, level, type, cost, duration, magic.basic, magic.advanced, magic.expert, magic.img \
                                   FROM  magic \
                                   WHERE magic.id = '{self.attribute}' AND \
                                        EXISTS (SELECT skill.name \
                                                FROM magic, skill \
                                                WHERE magic.element = skill.id)")
        return self._handle_magic(data[0], back_button_callback)

    def _handle_magic(self, magic, back_button_callback):
        if magic[5]:
            if magic[5] == "СМ":
                duration = "число ходов равное силе магии героя"
            else:
                duration = magic[5]
        else:
            duration = "нет"
        text = f'{magic[1]}\
        \n__________ \
        \nУровень: {magic[2]}\
        \n__________ \
        \nТип: {"боевое заклинание" if magic[3] == "C" else "походное заклинание"}\
        \n__________ \
        \nСтоимость: {magic[4]}\
        \n__________ \
        \nДлительность: {duration}\
        \n__________ \
        \nОбычный уровень: {magic[6]}\
        \n__________ \
        \nПродвинутый уровень: {magic[7]}\
        \n__________ \
        \nЭкспертный уровень: {magic[8]}'
        return self._return_image_and_keyboard(str(magic[9]), text, back_button_callback)

    def _get_skill(self, back_button_callback):
        data = connector.execute(f"SELECT id, name, no_skill, basic, advanced, expert, img \
                                   FROM  skill \
                                   WHERE id = '{self.attribute}'")
        return self._handle_skill(data[0], back_button_callback)

    def _handle_skill(self, skill, back_button_callback):
        text = f'{skill[1]}\
        \n__________ \
        \nНавык отсутствует: {skill[2]}\
        \n__________ \
        \nБазовый уровень: {skill[3]}\
        \n__________ \
        \nПродвинутый уровень: {skill[4]}\
        \n__________ \
        \nЭкспертный уровень: {skill[5]}'
        return self._return_image_and_keyboard(str(skill[6]), text, back_button_callback)

    def find(self, callback, back_button_callback = None):
        self._handle_callback(callback)
        method_name = "_get_" + self.table_name
        method = getattr(self, method_name)
        return method(back_button_callback)

    '''
    def _get_table_names(self):
        data = connector.execute(f"SELECT name FROM sqlite_master WHERE type = 'table'")
        return [item[0] for item in data]
    '''

    def _search_by_name(self, str_to_search):
        result = []
        if len(str_to_search) > 2:
            for table in self.tables_to_search:
                data = connector.execute(f"SELECT id, name \
                                        FROM {table} \
                                        WHERE UPPER(name) LIKE UPPER('%{str_to_search}%') \
                                                OR name LIKE '%{str_to_search.capitalize()}%'")
                for item in data:
                    result.append((item[1], table + "_" + str(item[0])))
        return result

    def search(self, str_to_search):
        data = self._search_by_name(str_to_search)
        rows = []
        if not data:
            return None
        elif len(data) == 1:
            return self.find(data[0][1])
        else:
            for item in data:
                rows.append([button(item[0], item[1])])
            return [keyboard("Резулаьтаты поиска:", rows)]

search = SearchClass()