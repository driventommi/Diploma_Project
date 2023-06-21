import json


def get_button(text, color):
    return {
        "action": {
            "type": "text",
            "payload": "{\"button\": \"" + "1" + "\"}",
            "label": f"{text}"
        },
        "color": f"{color}"
    }


keyboard = {
    "one_time": True,
    "buttons": [
        [get_button('Поиск', 'primary'), get_button('Пока', 'secondary')]
    ]
}


keyboard_second = {
    "one_time": True,
    "buttons": [
        [get_button('Да', 'primary'), get_button('Нет', 'primary')]
    ]
}


keyboard_next = {
    "one_time": True,
    "buttons": [
        [get_button('Дальше', 'primary'),get_button('Пока', 'secondary')]
    ]
}

keyboard_error = {
    "one_time": True,
    "buttons": [
        [get_button('Поиск', 'primary')]
    ]
}
keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))
keyboard_second = json.dumps(keyboard_second, ensure_ascii=False).encode('utf-8')
keyboard_second = str(keyboard_second.decode('utf-8'))
keyboard_next = json.dumps(keyboard_next, ensure_ascii=False).encode('utf-8')
keyboard_next = str(keyboard_next.decode('utf-8'))
keyboard_error = json.dumps(keyboard_error, ensure_ascii=False).encode('utf-8')
keyboard_error = str(keyboard_error.decode('utf-8'))