from vk_api import VkApi
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import json


class VK_chat_keys:
    def __init__(self, vk_session, vk, longpoll):

        self.vk_session = vk_session
        self.vk = vk
        self.longpoll = longpoll

    # описание и создание клавиатуры
    def keyboard(self):
        # определяем тип кнопок
        settings = dict(one_time=False, inline=True)
        keyboard = VkKeyboard(**settings)

        keys_struct = ({
                           'label': "Следующий пользователь",
                           'color': VkKeyboardColor.PRIMARY,
                           '_type': "forward"
                       },
                       {
                           'label': "Предыдущий пользователь",
                           'color': VkKeyboardColor.PRIMARY,
                           '_type': "backward"
                       },
                       {
                           'label': "Добавить в избранное",
                           'color': VkKeyboardColor.POSITIVE,
                           '_type': "like"
                       },
                       {
                           'label': "Добавить в черный список",
                           'color': VkKeyboardColor.NEGATIVE,
                           '_type': "ban"
                       },
                       {
                           'label': "Показать избранных",
                           'color': VkKeyboardColor.POSITIVE,
                           '_type': "show_favorite"
                       },
                       {
                           'label': "Закрыть",
                           'color': VkKeyboardColor.NEGATIVE,
                           '_type': "quit"
                       })

        for key in keys_struct:
            keyboard.add_callback_button(label=key['label'], color=key['color'], payload={"type": key['_type']})
            if keys_struct.index(key) + 1 != len(keys_struct):
                keyboard.add_line()

        return keyboard

    def additional_key(self):
        # определяем тип кнопок для вспомогательного меню - возврат из списка избранных
        settings = dict(one_time=False, inline=True)
        aux_keyboard = VkKeyboard(**settings)

        # создаем кнопку
        aux_keyboard.add_callback_button(label="Вернуться к поиску партнеров", color=VkKeyboardColor.PRIMARY,
                                         payload={"type": "return"})

        return aux_keyboard

    def exit_key(self):
        # определяем тип кнопки - закрыть
        settings = dict(one_time=False, inline=True)
        exit_keyboard = VkKeyboard(**settings)

        # создаем кнопку
        exit_keyboard.add_callback_button(label="Закрыть", color=VkKeyboardColor.NEGATIVE, payload={"type": "quit"})

        return exit_keyboard

    def pop_up(self, user_id, event_id, msg):
        payload = {
            'type': 'show_snackbar',
            'text': msg
        }

        resp = self.vk.messages.sendMessageEventAnswer(
            event_id=event_id,
            user_id=user_id,
            peer_id=user_id,
            event_data=json.dumps(payload))