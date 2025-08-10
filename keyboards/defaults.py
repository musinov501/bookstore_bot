from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from config import ADMINS
from typing import Optional

def phone_button():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton("📞Raqamni yuborish", request_contact=True)
    markup.add(btn)
    return markup



def make_buttons(names: list, row_width: int = 2, back: bool = False, admin_id: Optional[int] = None):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=row_width)
    buttons = []
    for name in names:
        btn = KeyboardButton(name)
        buttons.append(btn)
    markup.add(*buttons)


    if back:
        btn = KeyboardButton("⬅️Ortga")
        markup.add(btn)

    return markup