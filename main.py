import telebot
import pyautogui as pag
from telebot import types
import cv2
import numpy as np
import moviepy.editor as moviepy

bot = telebot.TeleBot("TOKEN")
print("Запуск бота...")


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Скриншот")
    btn2 = types.KeyboardButton("Запись экрана")
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id, "👋 Привет!", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_status(message):
    if message.text == 'Скриншот':
        bot.send_message(message.from_user.id, 'Скриншот отправляется...')
        pag.screenshot('scr.png')
        file = open('scr.png', 'rb')
        bot.send_photo(message.from_user.id, file)
    elif message.text == 'Запись экрана':
        bot.send_message(message.chat.id, "Запись видео... (ожидайте)")
        output = "video.mp4"
        img = pag.screenshot()
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        height, width, chhannels = img.shape

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output, fourcc, 20.00, (width, height))
        frames = 0

        while frames < 100:
            try:
                frames += 1
                img = pag.screenshot()
                image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                out.write(image)
                StopIteration(0.5)
            except KeyboardInterrupt:
                break
        out.release()
        cv2.destroyAllWindows()
        clip = moviepy.VideoFileClip("video.mp4")
        clip.write_videofile("video1.mp4")
        video = open('video1.mp4', 'rb')
        bot.send_video(message.chat.id, video, timeout=None)
    else:
        bot.send_message(message.from_user.id, "Извини, я не понимаю тебя(")

print('Бот запущен!')

bot.delete_webhook(drop_pending_updates=True)
bot.polling(none_stop=True)
