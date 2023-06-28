
import vk_api
from vk_api.longpoll import VkEventType
from vk_api.utils import get_random_id
from keyboard import keyboard, keyboard_next, keyboard_error

from config import community_token
from main import search_params, find_photos, add_in_db, find_match, compare, get_parameters, send_reply, longpoll

# Запуск
class BotInterface:

    def __init__(self, community_token):
        self.vk_session = vk_api.VkApi(token=community_token)
        self.parameters = None

    def message_send(self, user_id, message, attachment=None):
        self.vk_session.method('messages.send',
                               {'user_id': user_id,
                                'message': message,
                                'attachment': attachment,
                                'random_id': get_random_id()
                                }
                               )

    def send_reply(self, id, reply_text, kb=None, attachment=None):
        self.vk_session.method("messages.send",
                               {"user_id": id,
                                "message": reply_text,
                                "random_id": get_random_id(),
                                "keyboard": kb,
                                "attachment": attachment
                                })

    def event_handler(self):
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                message = event.text.lower()
                id = event.user_id
                kb = keyboard
                self.parameters = get_parameters(id)
                parameters = self.parameters[0]

                try:
                    if message == "привет":
                        send_reply(id, f"Привет, {parameters['first_name']}! Я бот знакомств ВК", keyboard)
                        send_reply(id, "Чтобы начать поиск людей - напиши мне Поиск")
                        send_reply(id, "Если захочешь остановить поиск на сегодня - напиши мне Пока")

                    elif message == "пока":
                        send_reply(id, "Пока:'(")

                    elif message == "hi":
                        send_reply(id, "Я умею разговариать только на русском:(( прости")

                    elif message == "bye":
                        send_reply(id, "Я умею разговариать только на русском:(( прости")

                    elif message == "поиск":
                        offset = 0
                        params_list = search_params(id, parameters['bdate'], parameters['sex'], parameters['city_data'])

                        users = find_match(id, params_list[0], params_list[1], (params_list[2]), (params_list[3]))

                        if users:
                            user = users.pop()
                            result = compare(id, user['id'])
                            if result is not True:
                                user_photos_all = find_photos(user['id'])
                                ph_attachment = ''
                                for number, photo in enumerate(user_photos_all):
                                    ph_attachment += f'photo{photo["owner_id"]}_{photo["id"]},'
                                    if number == 2:
                                        break
                                send_reply(id, f"Смотри кого я нашел: {user['name']} {user['user_link ']}",
                                           keyboard_next,
                                           attachment=ph_attachment)
                                send_reply(id, "Напиши дальше")
                                add_in_db(id, user['id'])
                            else:
                                send_reply(id, "Упс, эту анкету я уже показывал, нажми или напиши ДАЛЬШЕ",
                                           keyboard_next)
                                continue

                    elif message == "дальше":
                        if users:
                            user = users.pop()
                            result = compare(id, user['id'])
                            if result is not True:
                                user_photos_all = find_photos(user['id'])
                                ph_attachment = ''
                                for number, photo in enumerate(user_photos_all):
                                    ph_attachment += f'photo{photo["owner_id"]}_{photo["id"]},'
                                    if number == 2:
                                        break
                                send_reply(id, f"Смотри кого я нашел: {user['name']} {user['user_link ']}",
                                           keyboard_next,
                                           attachment=ph_attachment)
                                send_reply(id, "Напиши дальше")
                                add_in_db(id, user['id'])
                            else:
                                send_reply(id, "Упс, эту анкету я уже показывал, нажми или напиши ДАЛЬШЕ",
                                           keyboard_next)

                        else:
                            offset += 10
                            users = (
                                find_match(id, params_list[0], params_list[1], (params_list[2]), (params_list[3]),
                                           offset))
                            if users:
                                user = users.pop()
                                result = compare(id, user['id'])
                                if result is not True:
                                    user_photos_all = find_photos(user['id'])
                                    ph_attachment = ''
                                    for number, photo in enumerate(user_photos_all):
                                        ph_attachment += f'photo{photo["owner_id"]}_{photo["id"]},'
                                        if number == 2:
                                            break

                                    send_reply(id, f"Смотри кого я нашел: {user['name']} {user['user_link ']}",
                                               keyboard_next,
                                               attachment=ph_attachment)
                                    send_reply(id, "Напиши дальше")
                                    add_in_db(id, user['id'])
                                else:
                                    send_reply(id,
                                               "Упс, эту анкету я уже показывал, нажми или напиши ДАЛЬШЕ",
                                               keyboard_next)

                    else:
                        send_reply(id,
                                   f"Не понимаю тебя! Попробуй написать что-то другое, {parameters['first_name']}",
                                   keyboard_error)

                except (KeyError, NameError, TypeError):
                    send_reply(id, f"Не понимаю тебя! Попробуй написать что-то другое",
                               keyboard_error)


# if __name__ == '__main__':
bot = BotInterface(community_token)
bot.event_handler()
