class Message(object):
    def __init__(self, update):
        self.message_id = update['message']['message_id']
        self.chat_id = update['message']['chat']['id']
        self.chat_first_name = update['message']['chat']['first_name']
        self.username = update['message']['chat']['username'] if 'username' in update['message']['chat'] else None
        self.text = update['message']['text'] if 'text' in update['message'] else None
        
class CallbackQuery(object):
    def __init__(self, update):
        self.message_id = update['callback_query']['message']['message_id']
        self.chat_id = update['callback_query']['message']['chat']['id']
        self.chat_first_name = update['callback_query']['message']['chat']['first_name']
        self.username = update['callback_query']['message']['chat']['username'] if 'username' in update['callback_query']['message']['chat'] else None
        self.text = update['callback_query']['message']['text'] if 'text' in update['callback_query']['message'] else None
        self.reply_markup = update['callback_query']['message']['reply_markup']
        self.data = update['callback_query']['data']
