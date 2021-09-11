'''

'''
from handler import handler
from custom_types import Message, CallbackQuery
from keyboards import keyboards
from search import search
from chats import chats
from commands import is_in_commands

def main():
    offset = None
    message = None
    cq = None
    sended_message = None

    while True:
        data = handler.get_updates(offset)
        for item in data:
            print(item)
            offset = item['update_id'] + 1
            if 'message' in item:
                message = Message(item)
                chats.check(message)
                #Удаляем ласт сообщение, отправленное ботом, если оно есть
                if chats.get_last_message_id():
                    handler.delete_message(message.chat_id, chats.get_last_message_id())
                #Проверка текста на наличие в командах и отправка сообщения, соответствующего команде
                kbrd_name = is_in_commands(message.text.lower())
                if kbrd_name:
                    sended_message = handler.send_message(message.chat_id, *keyboards[kbrd_name])
                #поиск по тексту и выдача результатов
                else:
                    search_result = search.search(message.text)
                    if not search_result:
                        #ничего не найдено
                        sended_message = handler.send_message(message.chat_id, *keyboards['search_failed'])
                    elif len(search_result) == 2:
                        #найден 1 результат
                        sended_message = handler.send_photo(message.chat_id, search_result[0], *search_result[1])
                    else:
                        #найдено больше 1 результата
                        sended_message = handler.send_message(message.chat_id, *search_result[0])
                        chats.set_reply_markup(search_result[0])
                    chats.set_search_was_used(True)
                if sended_message:
                    chats.set_last_message_id(sended_message['message_id'])
            elif 'callback_query' in item:
                cq = CallbackQuery(item)
                chats.check(cq)
                if cq.data in keyboards.keys() or cq.data == "search_results":
                    if chats.get_search_was_used():
                        handler.delete_message(cq.chat_id, cq.message_id)
                        if cq.data == "search_results":
                            sended_message = handler.send_message(cq.chat_id, *chats.get_reply_markup())
                        else:
                            sended_message = handler.send_message(cq.chat_id, *keyboards[cq.data])
                    else:
                        handler.edit_message(cq.chat_id, cq.message_id, *keyboards[cq.data])
                    chats.set_search_was_used(False)
                else:
                    if not chats.get_search_was_used():
                        result = search.find(cq.data, chats.get_prev_cq_data())
                    else:
                        result = search.find(cq.data, "search_results")
                    handler.delete_message(cq.chat_id, cq.message_id)
                    sended_message = handler.send_photo(cq.chat_id, result[0], *result[1])
                    chats.set_search_was_used(True)
                if sended_message:
                    chats.set_last_message_id(sended_message['message_id'])
                chats.set_prev_cq_data(cq.data)

if __name__ == "__main__":
    main()