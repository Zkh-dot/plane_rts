import telebot
bot = telebot.TeleBot('1059442764:AAFlPFEROwxIGxPIK8mgEmO-pusoG77docg')
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == 'Привет!':
        bot.send_message(message.from_user.id, 'Салам алейкум, брат!')
    else:
        bot.send_message(message.from_user.id, 'Что-то на латышском')

bot.polling(none_stop=True, interval=0)