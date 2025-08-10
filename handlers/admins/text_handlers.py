from telebot.types import Message, ReplyKeyboardRemove
from data.loader import db, bot
from config import ADMINS
from keyboards.defaults import make_buttons

admin_buttons_names = [
    "➕ Janr qo'shish",
    "✏️ Janr tahrirlash",
    "❌ Janr o'chirish",
    "➕ Kitob qo'shish",
    "✏️ Kitob tahrirlash",
    "❌ Kitob o'chirish"
]

GENRES = {}
EDIT_GENRE = {}
DELETE_GENRE = {}

BOOKS_TEMP = {}
EDIT_BOOK = {}
DELETE_BOOK = {}


@bot.message_handler(func=lambda msg: msg.text == "👮🏻‍♂️Admin buyruqlari")
def reaction_to_admin(message: Message):

    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if from_user_id in ADMINS:
        bot.send_message(chat_id, "Admin buyruqlari👇👇👇", reply_markup=make_buttons(admin_buttons_names, back=True, admin_id=from_user_id))



# Adding genre
@bot.message_handler(func=lambda message: message.text == "➕ Janr qo'shish")
def reaction_to_admin(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if from_user_id in ADMINS:
        msg = bot.send_message(chat_id, "🎭Janr nomini kiriting")
        bot.register_next_step_handler(msg, get_genre_name)


def get_genre_name(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if from_user_id not in GENRES:
        GENRES[from_user_id] = []

    GENRES[from_user_id].append(message.text)


    msg = bot.send_message(chat_id, "Yana janr qo'shasizmi?", reply_markup=make_buttons(["Yes", "No"]))
    bot.register_next_step_handler(msg, save_genre)

def save_genre(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id

    if message.text == "No":

        for genre_name in GENRES[from_user_id]:
            db.insert_genre(genre_name)

        del GENRES[from_user_id]
        bot.send_message(chat_id, "Janrlar muvaffaqiyatli saqlandi!!!✅", reply_markup=make_buttons(admin_buttons_names, back=True))
    elif message.text == 'Yes':
        msg = bot.send_message(chat_id, "🎭Janr nomini kiriting")
        bot.register_next_step_handler(msg, get_genre_name)

# Editing genre
@bot.message_handler(func=lambda msg: msg.text == "✏️ Janr tahrirlash")
def edit_genre(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id

    if from_user_id in ADMINS:
        genres = db.select_genres()
        if not genres:
            bot.send_message(chat_id, "Hozircha hech qanday janr mavjud emas.")
            return

        buttons = [f"{genre[0]}. {genre[1]}" for genre in genres]
        msg = bot.send_message(chat_id, "Qaysi janrni tahrirlashni xohlaysiz?", reply_markup=make_buttons(buttons, back=True))
        bot.register_next_step_handler(msg, choose_genre_to_edit)



def choose_genre_to_edit(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id

    try:
        genre_id = int(message.text.split(".")[0])
    except:
        bot.send_message(chat_id, "Iltimos, ro‘yxatdan ID bo‘yicha tanlang.")
        return

    EDIT_GENRE[from_user_id] = genre_id
    msg = bot.send_message(chat_id, "Yangi janr nomini kiriting👇👇👇")
    bot.register_next_step_handler(msg, save_edited_genre)

def save_edited_genre(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id


    genre_id = EDIT_GENRE.get(from_user_id)
    new_name = message.text

    if genre_id:
        db.update_genre(genre_id, new_name)
        bot.send_message(chat_id, "✅ Janr muvaffaqiyatli tahrirlandi!", reply_markup=make_buttons(admin_buttons_names, back=True))
        del EDIT_GENRE[from_user_id]
    else:
        bot.send_message(chat_id, "Xatolik: janr topilmadi.")

#Removing genre
@bot.message_handler(func=lambda message: message.text == "❌ Janr o'chirish")
def delete_genre(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id


    if from_user_id in ADMINS:
        genres = db.select_genres()
        if not genres:
            bot.send_message(chat_id, "❗ Hozircha hech qanday janr mavjud emas.")
            return

        buttons = [f"{genre[0]}. {genre[1]}" for genre in genres]
        msg = bot.send_message(chat_id, "Qaysi janrni o'chirmoqchisiz?", reply_markup=make_buttons(buttons, back=True))
        bot.register_next_step_handler(msg, choose_genre_to_delete)


def choose_genre_to_delete(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id

    try:
        genre_id = int(message.text.split(".")[0])
    except:
        bot.send_message(chat_id, "⚠️ Iltimos, ro‘yxatdan to‘g‘ri tanlang.")
        return

    DELETE_GENRE[from_user_id] = genre_id
    msg = bot.send_message(chat_id, "O‘chirishni tasdiqlaysizmi?", reply_markup=make_buttons(["Yes", "No"], back=True))
    bot.register_next_step_handler(msg, confirm_delete_genre)


def confirm_delete_genre(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id

    if message.text == "Yes":
        genre_id = DELETE_GENRE.get(from_user_id)
        if genre_id:
            db.delete_genre(genre_id)
            bot.send_message(chat_id, "✅ Janr o‘chirildi!", reply_markup=make_buttons(admin_buttons_names, back=True))
        else:
            bot.send_message(chat_id, "❌ Xatolik: janr topilmadi.")

    else:
        bot.send_message(chat_id, "❌ O‘chirish bekor qilindi.", reply_markup=make_buttons(admin_buttons_names, back=True))

    DELETE_GENRE.pop(from_user_id, None)

#Adding book
@bot.message_handler(func=lambda msg: msg.text == "➕ Kitob qo'shish")
def add_book(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id

    if from_user_id in ADMINS:
        genres = db.select_genres()
        if not genres:
            bot.send_message(chat_id, "❗ Hozircha hech qanday janr mavjud emas. Avval janr qo‘shing.")
            return

        buttons = [f"{genre[0]}. {genre[1]}" for genre in genres]
        msg = bot.send_message(chat_id, "📚 Qaysi janrga kitob qo‘shmoqchisiz?",
                               reply_markup=make_buttons(buttons, back=True))
        bot.register_next_step_handler(msg, choose_genre_for_book)


def choose_genre_for_book(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    try:
        genre_id = int(message.text.split(".")[0])
    except:
        bot.send_message(message.chat.id, "⚠️ Iltimos, ro‘yxatdan to‘g‘ri tanlang.")
        return


    BOOKS_TEMP[from_user_id] = {'genre_id': genre_id}
    msg = bot.send_message(chat_id, "✏️ Kitob nomini kiriting:")
    bot.register_next_step_handler(msg, get_book_name)


def get_book_name(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    BOOKS_TEMP[from_user_id]['name'] = message.text
    msg = bot.send_message(chat_id, "👨‍💼 Muallif ismini kiriting:")
    bot.register_next_step_handler(msg, get_book_author)


def get_book_author(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    BOOKS_TEMP[from_user_id]['author'] = message.text
    msg = bot.send_message(chat_id, "📝 Kitob haqida qisqacha izoh kiriting:")
    bot.register_next_step_handler(msg, get_book_description)


def get_book_description(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    BOOKS_TEMP[from_user_id]['description'] = message.text
    msg = bot.send_message(chat_id, "📅 Kitob chiqarilgan yil yoki sanani kiriting:")
    bot.register_next_step_handler(msg, get_book_release_date)


def get_book_release_date(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    BOOKS_TEMP[from_user_id]['date_of_release'] = message.text
    msg = bot.send_message(chat_id, "📷 Kitob muqovasini yuboring (rasm):")
    bot.register_next_step_handler(msg, get_book_cover)


def get_book_cover(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id

    if message.photo:
        cover_photo = message.photo[-1].file_id
    else:
        cover_photo = None

    BOOKS_TEMP[from_user_id]['cover_photo'] = cover_photo


    data = BOOKS_TEMP[from_user_id]

    db.insert_book(
        data['genre_id'],
        data['name'],
        data['author'],
        data['description'],
        data['date_of_release'],
        data['cover_photo']
    )

    bot.send_message(chat_id, f"✅ Kitob -> |{data['name']}| muvaffaqiyatli qo'shildi!!", reply_markup=make_buttons(admin_buttons_names, back=True))

    BOOKS_TEMP.pop(from_user_id, None)

#Editing book

@bot.message_handler(func=lambda msg: msg.text == "✏️ Kitob tahrirlash")
def edit_book(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id

    if from_user_id in ADMINS:
        books = db.select_books()
        if not books:
            bot.send_message(chat_id, "📚 Hozircha hech qanday kitob yo‘q.")
            return

        buttons = [f"{book[0]}. {book[1]}" for book in books]
        msg = bot.send_message(chat_id, "✏️ Qaysi kitobni tahrirlamoqchisiz?", reply_markup=make_buttons(buttons, back=True))
        bot.register_next_step_handler(msg, choose_book_to_edit)

def choose_book_to_edit(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id

    try:
        book_id = int(message.text.split(".")[0])
    except:
        bot.send_message(message.chat.id, "⚠️ Iltimos, ro‘yxatdan to‘g‘ri tanlang.")
        return

    book = db.get_book_by_id(book_id)
    if not book:
        bot.send_message(chat_id, "❗ Kitob topilmadi.")
        return


    EDIT_BOOK[from_user_id] = {
        'id': book[0],
        'genre_id': book[1],
        'name': book[2],
        'author': book[3],
        'description': book[4],
        'date_of_release': book[5],
        'cover_photo': book[6]
    }

    text = (
        f"📖 Kitob: {book[2]}\n"
        f"👨‍💼 Muallif: {book[3]}\n"
        f"📝 Izoh: {book[4]}\n"
        f"📅 Chiqarilgan sana: {book[5]}\n\n"
        "Qaysi qismni tahrirlamoqchisiz?"
    )


    msg = bot.send_message(chat_id, text, reply_markup=make_buttons(["📖 Nom", "👨‍💼 Muallif", "📝 Izoh", "📅 Sana", "📷 Muqova", "✅ Saqlash"]))
    bot.register_next_step_handler(msg, choose_thing_to_edit)


def choose_thing_to_edit(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    choice = message.text

    if choice == "📖 Nom":
        msg = bot.send_message(message.chat.id, "Yangi nomni kiriting:")
        bot.register_next_step_handler(msg, set_book_name)

    elif choice == "👨‍💼 Muallif":
        msg = bot.send_message(message.chat.id, "Yangi muallifni kiriting:")
        bot.register_next_step_handler(msg, set_book_author)

    elif choice == "📝 Izoh":
        msg = bot.send_message(message.chat.id, "Yangi izohni kiriting:")
        bot.register_next_step_handler(msg, set_book_description)

    elif choice == "📅 Sana":
        msg = bot.send_message(message.chat.id, "Yangi chiqarilgan sanani kiriting (YYYY yoki YYYY-MM-DD):")
        bot.register_next_step_handler(msg, set_book_date)

    elif choice == "📷 Muqova":
        msg = bot.send_message(message.chat.id, "Yangi muqova rasmni yuboring:")
        bot.register_next_step_handler(msg, set_book_cover)


    elif choice == "✅ Saqlash":
        data = EDIT_BOOK[from_user_id]
        db.update_book(data['id'], data['name'], data['author'], data['description'], data['date_of_release'], data['cover_photo'])
        bot.send_message(chat_id, "✅ Kitob ma'lumotlari yangilandi!", reply_markup=make_buttons(admin_buttons_names, back=True))
    else:
        bot.send_message(message.chat.id, "⚠️ Noto‘g‘ri tanlov.")


def set_book_name(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    EDIT_BOOK[from_user_id]['name'] = message.text
    bot.send_message(message.chat.id, "✅ Nom yangilandi.")
    show_edit_menu(chat_id)


def set_book_author(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    EDIT_BOOK[from_user_id]['author'] = message.text
    bot.send_message(message.chat.id, "✅ Muallif yangilandi.")
    show_edit_menu(chat_id)


def set_book_description(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    EDIT_BOOK[from_user_id]['description'] = message.text
    bot.send_message(message.chat.id, "✅ Izoh yangilandi.")
    show_edit_menu(chat_id)


def set_book_date(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    EDIT_BOOK[from_user_id]['date_of_release'] = message.text
    bot.send_message(message.chat.id, "✅ Sana yangilandi.")
    show_edit_menu(chat_id)



def set_book_cover(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if message.photo:
        EDIT_BOOK[from_user_id]['cover_photo'] = message.photo[-1].file_id
        bot.send_message(message.chat.id, "✅ Rasm yangilandi.")
    else:
        bot.send_message(message.chat.id, "⚠️ Iltimos, rasm yuboring.")
    show_edit_menu(chat_id)


def show_edit_menu(chat_id):
    edit_buttons = ["📖 Nom", "👨‍💼 Muallif", "📝 Izoh", "📅 Sana", "📷 Muqova", "✅ Saqlash"]
    msg = bot.send_message(chat_id, "Qaysi qismni tahrirlamoqchisiz?",
                           reply_markup=make_buttons(edit_buttons, row_width=2))
    bot.register_next_step_handler(msg, choose_thing_to_edit)

#Removing Book

@bot.message_handler(func=lambda message: message.text == "❌ Kitob o'chirish")
def delete_book(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id

    if from_user_id in ADMINS:
        books = db.select_books()
        if not books:
            bot.send_message(chat_id, "📚 Hozircha hech qanday kitob yo‘q.")
            return

        buttons = [f"{book[0]}. {book[1]}" for book in books]
        msg = bot.send_message(chat_id, "❌ Qaysi kitobni o'chirmoqchisiz?",
                               reply_markup=make_buttons(buttons, back=True))
        bot.register_next_step_handler(msg, choose_book_to_delete)


def choose_book_to_delete(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id

    if message.text == "⬅️Ortga":
        bot.send_message(chat_id, "Admin panelga qaytdingiz.",
                         reply_markup=make_buttons(admin_buttons_names, back=True))
        return

    try:
        book_id = int(message.text.split(".")[0])
    except:
        bot.send_message(chat_id, "⚠️ Iltimos, ro‘yxatdan to‘g‘ri tanlang.")
        return


    book = db.get_book_by_id(book_id)
    if not book:
        bot.send_message(chat_id, "❗ Kitob topilmadi.")
        return

    DELETE_BOOK[from_user_id] = book_id
    msg = bot.send_message(chat_id, f"Kitob: {book[2]}\nIshonchingiz komilmi?", reply_markup=make_buttons(["Ha", "Yo'q"]))
    bot.register_next_step_handler(msg, confirm_delete_book)


def confirm_delete_book(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id

    answer = message.text.lower()

    if answer == 'ha':
        book_id = DELETE_BOOK.get(from_user_id)
        if book_id:
            db.delete_book(book_id)
            bot.send_message(chat_id, "✅ Kitob muvaffaqiyatli o'chirildi!",reply_markup=make_buttons(admin_buttons_names, back=True) )
        else:
            bot.send_message(chat_id, "❗ Hech qanday kitob tanlanmagan.")

    elif answer == "yo'q":
        bot.send_message(chat_id, "❌ O'chirish bekor qilindi.",
                         reply_markup=make_buttons(admin_buttons_names, back=True))

    else:
        bot.send_message(chat_id, "⚠️ Iltimos, Ha yoki Yo‘q deb javob bering.")
        bot.register_next_step_handler(message, confirm_delete_book)