from telebot.types import Message, BotCommand, ReplyKeyboardRemove
from data.loader import db, bot
from keyboards.defaults import phone_button, make_buttons
from config import ADMINS


REGISTER = {}


bot.set_my_commands([
    BotCommand('start', 'Botni ishga tushirish'),
    BotCommand('help', 'Yordam')

])


@bot.message_handler(commands=['start'])
def start(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    full_name = message.from_user.full_name

    user = db.get_user(from_user_id)
    if from_user_id  in ADMINS:
        text = f"👨‍💼 Salom, admin {full_name}!\nAdmin panelga xush kelibsiz."
        bot.send_message(chat_id, text, reply_markup=make_buttons(["👮🏻‍♂️Admin buyruqlari"]))
    else:
        if not user:
            db.insert_telegram_id(from_user_id)
            text = (f"Assalomu alaykum {full_name}\n📚Online Kutubxonamizga xush kelibsiz!😊😊\n\n Avval ro'yxatdan o'ting:\n"
            f"To'liq ismingizni kiriting👇👇👇")
            msg = bot.send_message(chat_id, text)
            bot.register_next_step_handler(msg, get_name)

        else:
            genres_tuples = db.select_genres()
            genres_names = [genre[1] for genre in genres_tuples]
            bot.send_message(chat_id, "O'zingizga kerak bo'lgan janrni tanlang👇👇👇", reply_markup=make_buttons(genres_names))



def get_name(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id

    if message.text == '/start':
        bot.send_message(chat_id, "Bekor qilindi!!!")
    else:
        full_name = message.text
        REGISTER[from_user_id] = {
            'full_name': full_name
        }

        msg = bot.send_message(chat_id, "Pastdagi tugmani bosib, telefon raqamingizni yuboring👇👇👇", reply_markup=phone_button())
        bot.register_next_step_handler(msg, get_phone)


def get_phone(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id

    if message.contact:
        phone_number = message.contact.phone_number
        full_name = REGISTER[from_user_id]['full_name']
        genres_tuples = db.select_genres()
        genres_names = [genre[1] for genre in genres_tuples]
        db.update_user(from_user_id, full_name, phone_number)
        bot.send_message(chat_id, "Tabriklaymiz siz ro'yxatdan o'tdingiz 🎉🎉🎉", reply_markup=ReplyKeyboardRemove())
        bot.send_message(chat_id, "O'zingizga kerak bo'lgan ma'lumotni tanlang👇👇👇", reply_markup=make_buttons(genres_names))
    else:
        if message.text == '/start':
            bot.send_message(chat_id, "Bekor qilindi!!!")
        else:
            msg = bot.send_message(chat_id, "Pastdagi tugmani bosib, telefon raqamingizni yuboring👇👇👇",
                                   reply_markup=phone_button())
            bot.register_next_step_handler(msg, get_phone)



@bot.message_handler(commands=['help'])
def reaction_to_help(message: Message):
    chat_id = message.chat.id
    text = f'''📚 Xush kelibsiz!  
Bu bot orqali siz kitoblarni janrlar bo‘yicha ko‘rib chiqishingiz va ular haqida batafsil ma’lumot olishingiz mumkin.\n\n

👤 Foydalanuvchilar uchun:\n
- Janr tugmasini bosing → tegishli kitoblar ro‘yxati chiqadi.\n
- Kitob nomini bosing → nom, muallif, izoh, chiqarilgan sana va muqova fotosini ko‘rasiz.\n
- ⬅️Ortga tugmasi orqali asosiy menyuga qaytishingiz mumkin.\n\n

👮🏻‍♂️ Administratorlar uchun:\n
- 📌 Janr va kitoblarni qo‘shish, tahrirlash yoki o‘chirish.\n
- Admin panelga kirish uchun “👮🏻‍♂️Admin buyruqlari” tugmasini bosing.\n\n

ℹ️ Foydali maslahatlar:\n
- Kitob qidirishda to‘g‘ri nomini kiriting.\n
- Sanalarni YYYY yoki YYYY-MM-DD formatida yozing.\n
- Muqova rasmlari sifatli bo‘lishi tavsiya etiladi.\n\n

❓ Savollaringiz bo‘lsa, admin bilan bog‘laning: @musinov_501\n'''

    bot.send_message(chat_id, text)