from random import randrange
from config import*
from keyboard import keyboard, keyboard_second, keyboard_next, keyboard_error
from DB_core import add_in_db, compare

import datetime
import vk_api
import requests

from vk_api.longpoll import VkLongPoll, VkEventType


vk_session = vk_api.VkApi(token=community_token)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


# ф-я отправки сообщений ботом
def send_reply(id, reply_text, kb=None, attachment=None):
    vk_session.method("messages.send",
                      {"user_id": id,
                       "message": reply_text,
                       "random_id": randrange(10 ** 7),
                       "keyboard": kb,
                       "attachment": attachment
                       })


# ф-я определения параметров пользователя ботом
def get_parameters(user_id):
    url = "https://api.vk.com/method/users.get"
    params = {
        "access_token": user_token,
        "user_ids": user_id,
        "v": "5.131",
        "fields": "first_name, sex, bdate, city"
    }
    rep = requests.get(url, params=params)
    response = rep.json()
    try:
        data_dict = response['response']

        parameters_l = []

        for dictionary in data_dict:
            parameters_l.append({'first_name': dictionary['first_name'],
                                 'sex': dictionary['sex'],
                                 'bdate': dictionary['bdate'],
                                 'city_data': dictionary['city']
                                 })
        return parameters_l
    except KeyError:
        send_reply(id, "У меня возникла ошибка")


# ф-я смена пола для поиска
def sex_type(user_id, sex):
    try:
        sex = sex
        if sex == 2:
            look_up_sex = 1
            return look_up_sex
        elif sex == 1:
            look_up_sex = 2
            return look_up_sex
    except KeyError:
        send_reply(user_id, "У меня возникла ошибка")


# ф-я определения минимального возраста с ограничениями
def ask_min_age(user_id, bdate):
    try:
        birth_date = bdate
        if birth_date is not None:
            birth_date_list = birth_date.split('.')
            if len(birth_date_list) == 3:
                year = int(birth_date_list[2])
                today_year = int(datetime.date.today().year)
                user_age = today_year - year
                send_reply(user_id, f"Тебе сейчас {user_age} лет! Установим этот возраст минимальным?")
                send_reply(user_id, "Ответь Да или Нет", keyboard_second)
                for event in longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        message = event.text.lower()
                        if message == "да":
                            min_age = user_age
                            return min_age
                        elif message == "нет":
                            send_reply(user_id, "Введи минимальный возраст для поиска(минимум 18 лет):")
                            for event in longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                    if int(event.text) <= 17:
                                        send_reply(user_id, "Минимальный возраст для поиска - от 18 лет!")
                                        send_reply(user_id,
                                                   "Попробуй еще раз! Введи минимальный возраст для поиска(минимум 18 лет):")
                                    elif int(event.text) > 18:
                                        min_age = event.text
                                        return min_age
                                    else:
                                        send_reply(user_id, "Не понимаю тебя, попробуй еще раз")
                        else:
                            send_reply(user_id, "Не понимаю тебя, попробуй еще раз")
            if len(birth_date_list) == 2 or birth_date is None:
                send_reply(user_id, "Введи минимальный возраст для поиска(минимум 18 лет):")
                for event in longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        if int(event.text) <= 17:
                            send_reply(user_id, "Минимальный возраст для поиска - от 18 лет!")
                            send_reply(user_id,
                                       "Попробуй еще раз! Введи минимальный возраст для поиска(минимум 18 лет):")
                        elif int(event.text) > 18:
                            min_age = event.text
                            return min_age
                        else:
                            send_reply(user_id, "Не понимаю тебя, попробуй еще раз")
        else:
            send_reply(user_id, "Введи минимальный возраст для поиска(минимум 18 лет):")
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    if int(event.text) <= 17:
                        send_reply(user_id, "Минимальный возраст для поиска - от 18 лет!")
                        send_reply(user_id,
                                   "Попробуй еще раз! Введи минимальный возраст для поиска(минимум 18 лет):")
                    elif int(event.text) > 18:
                        min_age = event.text
                        return min_age
                    else:
                        send_reply(user_id, "Не понимаю тебя, попробуй еще раз")
    except (KeyError, NameError, TypeError):
        send_reply(id, f"Не понимаю тебя! Попробуй начать сначала", keyboard_error)


# ф-я максимального порога возраста
def ask_max_age(user_id):
    send_reply(user_id, "Введи максимальный возраст для поиска:")
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if event.text.isdigit() is not True:
                send_reply(user_id, "Вводите только цифры!")
            elif int(event.text) > 99:
                send_reply(user_id, "Боюсь люди столько не живут")
                send_reply(user_id, "Попробуй еще раз! Введи максимальный возраст для поиска:")
            else:
                max_age = event.text
                return max_age


# Поиск ID Города по названию
def city_id_search(user_id, city_name):
    url = "https://api.vk.com/method/database.getCities"
    params = {
        'access_token': user_token,
        'country_id': 1,
        'q': f'{city_name}',
        'need_all': 0,
        'count': 1000,
        'v': '5.131'
        }
    res = requests.get(url, params=params)
    response = res.json()

    try:
        data_list = response['response']
        all_cities = data_list['items']
        for i in all_cities:
            if i.get('title').lower() == city_name:
                found_city_id = i.get('id')
                return found_city_id
    except (KeyError, NameError, TypeError):
        send_reply(user_id, f"Не могу найти этот город! Попробуй заново", keyboard_error)


# Поиск города основной
def city_search(user_id, city_data):
    try:
        data_dict = city_data
        if data_dict:
            city_id = str(data_dict['id'])
            user_city_name = data_dict['title']
            send_reply(user_id, f"Твой город {user_city_name}, будем искать по нему?")
            send_reply(user_id, "Ответь Да или Нет", keyboard_second)
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    if event.text.lower() == "да":
                        return city_id
                    elif event.text.lower() == "нет":
                        send_reply(user_id, "Ок, тогда напиши название города в котором будем искать:")
                        for event in longpoll.listen():
                            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                if event.text.isdigit():
                                    send_reply(user_id, "Вводите только русские буквы!")
                                else:
                                    city_name = event.text.lower()
                                    city_id = city_id_search(user_id, city_name)
                                    return city_id
        else:
            send_reply(user_id, "Напиши название города в котором будем искать:")
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    if event.text.isdigit() is True:
                        send_reply(user_id, "Вводите только русские буквы!")
                    else:
                        city_name = event.text.lower()
                        city_id = city_id_search(user_id, city_name)
                        return city_id
    except (KeyError, NameError, TypeError):
        send_reply(user_id, f"Не понимаю тебя! Попробуй написать что-то другое", keyboard_error)


# ф-я сохранения усовий поиска для сессии
def search_params(user_id, date, sex, city_data):
    params_list = [sex_type(user_id, sex),
                   ask_min_age(user_id, date),
                   ask_max_age(user_id),
                   city_search(user_id, city_data)
                   ]
    return params_list


def find_photos(user_id):
    url = "https://api.vk.com/method/photos.get"
    params = {
        "access_token": user_token,
        "owner_id": user_id,
        "v": "5.131",
        "album_id": 'profile',
        "extended": 1
    }
    res = requests.get(url, params=params)
    response = res.json()
    try:
        all_list = response['response']
        photos = all_list['items']

    except KeyError:
        return []

    result = [{'owner_id': photo['owner_id'],
               'id': photo['id'],
               'likes': photo['likes']['count'],
               'comments': photo['comments']['count'],
               }
              for photo in photos
              ]
    result.sort(key=lambda x: x['likes'] + x['comments'] * 10, reverse=True)

    return result[:3]


# ф-я поиска пары по параметрам
def find_match(user_id, sex, age_from, age_to, city_s, offset=None):
    url = 'https://api.vk.com/method/users.search'
    params = {'access_token': user_token,
              'v': '5.131',
              'offset': offset,
              'sex': f"{sex}",
              'age_from': f"{age_from}",
              'age_to': f"{age_to}",
              'city': f"{city_s}",
              'fields': 'is_closed, id, first_name, last_name',
              'status': '1' or '6',
              'count': 10}
    resp = requests.get(url, params=params)
    resp_json = resp.json()
    try:
        resp_dict = resp_json['response']
        list_of_users = resp_dict['items']

        user_params = []

        for user_dict in list_of_users:
            if user_dict.get('is_closed') is False:
                user_params.append({'id': user_dict['id'],
                                    'name': user_dict['first_name'] + ' ' + user_dict['last_name'],
                                    'user_link ': 'vk.com/id' + (str(user_dict['id']) + ' ')
                                    })
            else:
                continue
        return user_params
    except (KeyError, NameError, TypeError):
        send_reply(user_id, f"Ошибка поиска! Попробуй написать что-то другое", keyboard_error)
