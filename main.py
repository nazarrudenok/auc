import telebot
import time
from config import TOKEN, conn

bot = telebot.TeleBot(TOKEN)

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    cht = message.chat.id
    bot.send_chat_action(cht, 'typing')
    time.sleep(0.8)
    bot.send_message(cht, f'Вітаю, <b>@{message.from_user.username}</b>!', parse_mode='HTML')
    time.sleep(0.8)

    bot.send_chat_action(cht, 'typing')
    time.sleep(0.75)
    msg = bot.send_message(cht, f'Давай заповнимо заявку, щоб виставити твій лот на аукціон', parse_mode='HTML')
    time.sleep(0.75)

    bot.send_chat_action(cht, 'typing')
    time.sleep(0.75)
    bot.send_message(cht, f'<b>Врахуй, що це коштуватиме 15 гривень</b>', parse_mode='HTML')
    time.sleep(0.75)

    bot.send_chat_action(cht, 'typing')
    time.sleep(0.75)
    bot.send_message(cht, f'<b>24 години аукціону - 15 гривень\n48 годин - 30 гривень</b>\nІ так далі... Гадаю, ти вмієш рахувати :)', parse_mode='HTML')
    time.sleep(0.75)

    bot.send_chat_action(cht, 'typing')
    time.sleep(0.75)
    bot.send_message(cht, f'Готовий?')
    time.sleep(0.75)

    bot.send_chat_action(cht, 'typing')
    time.sleep(0.75)
    bot.send_message(cht, f'Чудово!')
    time.sleep(0.75)

    bot.send_chat_action(cht, 'typing')
    time.sleep(0.75)
    msg = bot.send_message(cht, f'Тоді напиши як тебе звуть:')
    bot.register_next_step_handler(msg, func1)

def func1(message):
    cht = message.chat.id
    user_data[cht] = {
        'username': message.from_user.username,
        'real_name': message.text
    }

    bot.send_chat_action(cht, 'typing')
    time.sleep(0.75)
    bot.send_message(cht, f"Дякую! Гарне ім'я, до речі :)")
    time.sleep(0.75)

    bot.send_chat_action(cht, 'typing')
    time.sleep(0.75)
    msg = bot.send_message(cht, 'Тепер напиши статтю, яка буде описувати товар, який є на аукціоні:')
    bot.register_next_step_handler(msg, func2)

def func2(message):
    cht = message.chat.id
    user_data[cht]['article'] = message.text

    bot.send_chat_action(cht, 'typing')
    time.sleep(0.75)
    bot.send_message(cht, 'Чудово сказано! Думаю буде багато охочих взяти участь в аукціоні')
    time.sleep(0.75)

    bot.send_chat_action(cht, 'typing')
    time.sleep(0.75)
    bot.send_message(cht, 'Гаразд, тепер надішли фото товару')
    time.sleep(0.75)

    bot.send_chat_action(cht, 'typing')
    time.sleep(0.75)
    msg = bot.send_message(cht, '<b>Ти можеш надіслати лише 1 фото</b>', parse_mode='HTML')
    bot.register_next_step_handler(msg, func3)

def func3(message):
    cht = message.chat.id

    if message.photo:
        user_data[cht]['item_photo'] = message.photo[-1].file_id

        bot.send_chat_action(cht, 'typing')
        time.sleep(0.75)
        bot.send_message(cht, 'Супер!')
        time.sleep(0.75)

        bot.send_chat_action(cht, 'typing')
        time.sleep(0.75)
        bot.send_message(cht, 'Тепер тобі потібно оплатити пост та надіслати фото квитанції про оплату\n\n<b>Якщо ти не оплатиш або підробиш, надішлеш не ту квитанцію чи фото, твій пост буде видалено\n\nТакож за нецензурну лексику або неадекватний опис чи картинку, пост буде видалено\n\nКошти не повертаються</b>', parse_mode='HTML')
        time.sleep(0.75)

        bot.send_chat_action(cht, 'typing')
        time.sleep(0.75)
        bot.send_message(cht, f'Ось реквізити для оплати\nМожеш натиснути на номер карти, він скопіюється автоматично\n<pre>1111 2222 3333 4444</pre>', parse_mode='HTML')
        time.sleep(0.75)

        bot.send_chat_action(cht, 'typing')
        time.sleep(0.75)
        msg = bot.send_message(cht, f'Коли завершиш оплату, надішли фото квитанції. Я чекаю :)', parse_mode='HTML')
        bot.register_next_step_handler(msg, func4)

def func4(message):
    cht = message.chat.id

    if message.photo:
        user_data[cht]['receipt_photo'] = message.photo[-1].file_id

        username = user_data[cht]['username']
        real_name = user_data[cht]['real_name']
        article = user_data[cht]['article']
        item_photo_id = user_data[cht]['item_photo']
        receipt_photo_id = user_data[cht]['receipt_photo']
        #
        item_photo_info = bot.get_file(item_photo_id)
        downloaded_item_file = bot.download_file(item_photo_info.file_path)
        item_path = f'photos/item_photo.jpg'
        with open(item_path, 'wb') as f:
            f.write(downloaded_item_file)
        #
        #
        receipt_photo_info = bot.get_file(receipt_photo_id)
        downloaded_receipt_file = bot.download_file(receipt_photo_info.file_path)
        receipt_path = f'photos/receipt_photo.jpg'
        with open(receipt_path, 'wb') as f:
            f.write(downloaded_receipt_file)
        #

        try:
            with conn.cursor() as cursor:
                with open('photos/item_photo.jpg', 'rb') as p1:
                    with open('photos/receipt_photo.jpg', 'rb') as p2:
                        cursor.execute("INSERT INTO application (username, real_name, article, item_photo, receipt_photo) VALUES (%s, %s, %s, %s, %s)", (str(username), str(real_name), str(article), p1, p2))
                        conn.commit()

                        bot.send_message(1001173176, f"Name: {real_name}\nUsername: @{username}\nArticle: {article}")
                        bot.send_message(1001173176, f"item photo:")
                        bot.send_photo(1001173176, p1)
                        bot.send_message(1001173176, f"receipt photo:")
                        bot.send_photo(1001173176, p2)

                        bot.send_chat_action(cht, 'typing')
                        time.sleep(0.75)
                        bot.send_message(cht,f'Оце й усе! Дякую, що заповнив заявку, вона вже розміщена у телеграм каналі - @none\nНагадую, якщо оплати не було - пост невдовзі буде видалено',parse_mode='HTML')
                        time.sleep(0.75)

                        bot.send_chat_action(cht, 'typing')
                        time.sleep(0.75)
                        bot.send_message(cht, f'Ще раз дякую, щасливо!', parse_mode='HTML')


        except Exception as ex:
            bot.send_chat_action(cht, 'typing')
            time.sleep(0.75)
            bot.send_message(cht, f'Ось халепа! Звернись до розробника за допомогою - @nazarrudenok\nПомилка:\n{ex}')

    else:
        bot.send_chat_action(cht, 'typing')
        time.sleep(0.75)
        bot.send_message(cht, 'Халепа! Це не фото! Заповни заявку з почаку - /start')

bot.polling()