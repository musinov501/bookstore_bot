from data.loader import bot, db
import handlers


if __name__ == '__main__':
    db.create_table_users()
    db.create_table_genres()
    # db.drop_table_books()
    db.create_table_books()
    bot.infinity_polling()