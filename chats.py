from db_connector import connector
import json

class Chats(object):
    
    def _is_in_db(self):
        data = connector.execute(f"SELECT tg_id, name\
                                  FROM chat\
                                  WHERE tg_id = {self.chat_id}")
        if len(data):
            return True
        return False
    
    def _insert(self):
        data = (str(self.chat_id), self.chat_first_name)
        connector.execute_many("INSERT INTO chat (tg_id, name)\
                                VALUES (?, ?)", [data])

    def _update(self, column, value):
        connector.execute(f"UPDATE chat\
                           SET {column} = '{value}'\
                           WHERE tg_id = {self.chat_id}")
    
    def _get_value(self, column):
        result = connector.execute(f"SELECT {column}\
                                    FROM chat\
                                    WHERE tg_id = {self.chat_id}")
        return result[0][0]

    def check(self, item):
        self.chat_id = item.chat_id
        self.chat_first_name = item.chat_first_name
        self.username = item.username if item.username else ""
        if self._is_in_db():
            self._update("name", self.chat_first_name)
            self._update("username", self.username)
        else: 
            self._insert()

    def set_prev_cq_data(self, cq_data):
        self._update("prev_cq_data", cq_data)


    def set_reply_markup(self, markup):
        self._update("reply_markup", json.dumps(markup))

    def get_prev_cq_data(self):
        return self._get_value("prev_cq_data")
    
    def get_reply_markup(self):
        return json.loads(self._get_value("reply_markup"))

    def set_search_was_used(self, predicate):
        result = 1 if predicate else 0
        self._update("search_was_used", result)

    def get_search_was_used(self):
        return self._get_value("search_was_used")
    
    def set_last_message_id(self, message_id):
        self._update("last_message_id", message_id)

    def get_last_message_id(self):
        return self._get_value("last_message_id")

chats = Chats()