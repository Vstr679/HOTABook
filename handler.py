import requests
import json
from config import TOKEN

class HandlerClass():
    def __init__(self, token):
        self.api_url = f"https://api.telegram.org/bot{token}/"

    def get_updates(self, offset = None, timeout = 30):
        params = {"offset": offset, "timeout": timeout}
        response = requests.get(self.api_url + "getUpdates", params)
        if response.status_code == requests.codes.ok:
            return response.json()['result']

    def send_message(self, chat_id, text, reply_markup = None):
        if reply_markup == None:
            reply_markup = {}
        params = {'chat_id': chat_id, 'text': text, 'reply_markup': reply_markup}
        response = requests.post(self.api_url + "sendMessage", json = params)
        if response.status_code == requests.codes.ok:
            return response.json()['result']
    
    def edit_message(self, chat_id, message_id, text, reply_markup = None):
        if reply_markup == None:
            reply_markup = {}
        params = {'chat_id': chat_id, 'text': text, 'message_id': message_id, 'reply_markup': reply_markup}
        response = requests.post(self.api_url + "editMessageText", json = params)
        if response.status_code == requests.codes.ok:
            return response.json()['result']

    def send_photo(self, chat_id, photo, caption, reply_markup = None):
        if reply_markup == None:
            reply_markup = {}
        params = {'chat_id': chat_id, 'caption': caption, 'reply_markup': json.dumps(reply_markup)}
        response = requests.post(self.api_url + "sendPhoto", data = params, files = {'photo': photo})
        if response.status_code == requests.codes.ok:
            return response.json()['result']
    
    def delete_message(self, chat_id, message_id):
        params = {'chat_id': chat_id, 'message_id': message_id}
        response = requests.post(self.api_url + "deleteMessage", data = params)
        if response.status_code == requests.codes.ok:
            return response.json()['result']

handler = HandlerClass(TOKEN)