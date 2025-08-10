from telebot.types import Message
from data.loader import db, bot
from keyboards.defaults import make_buttons
from config import ADMINS
from handlers.admins.text_handlers import admin_buttons_names


@bot.message_handler(func = lambda message: db.genre_exists(message.text))
def show_books_by_genre(message: Message):
    chat_id = message.chat.id
    genre_name = message.text
    genre_id = db.get_genre_id(genre_name)
    books = db.select_books_by_genre(genre_id)


    if not books:
        bot.send_message(message.chat.id, "Bu janrda hali kitoblar mavjud emas.",
                         reply_markup=make_buttons(["⬅️Ortga"]))
        return


    book_names = [f"{book[1]}" for book in books]
    bot.send_message(chat_id,  f"📚 {genre_name} janridagi kitoblar:", reply_markup=make_buttons(book_names, back=True))


@bot.message_handler(func=lambda message: db.book_exists(message.text))
def show_book_info(message: Message):
    chat_id = message.chat.id
    book_name = message.text
    book = db.get_book_by_name(book_name)

    if not book:
        bot.send_message(message.chat.id, "Kitob topilmadi.")
        return

    id, name, author, description, date_of_release, cover_photo = book

    text = (
        f"📖 <b>{name}</b>\n"
        f"👨‍💼 <b>Muallif:</b> {author}\n"
        f"📝 <b>Izoh:</b> {description}\n"
        f"📅 <b>Chiqarilgan sana:</b> {date_of_release} yil"
    )

    bot.send_photo(chat_id, photo=cover_photo, caption=text, parse_mode='HTML')


@bot.message_handler(func=lambda message: message.text == "⬅️Ortga" )
def handle_back(message: Message):
        if message.from_user.id in ADMINS:
            bot.send_message(
                message.chat.id,
                "Admin panelga qaytdingiz.",
                reply_markup=make_buttons(admin_buttons_names, back=True, admin_id=message.from_user.id)
            )
        else:
            genres = db.select_genres()
            buttons = [f"{genre[1]}" for genre in genres]
            bot.send_message(
                message.chat.id,
                "Asosiy menyuga qaytdingiz.",
                reply_markup=make_buttons(buttons)
            )
        return True
