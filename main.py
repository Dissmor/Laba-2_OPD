import os

from aiogram.types import InputFile

from cfg import TOKEN, ADMIN_NAME, ADMIN_ID
import random
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
from datetime import datetime  ######################

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
data = []
users = []
adminName = ADMIN_NAME
adminId = ADMIN_ID
directory = 'assets'

@dp.message_handler(commands=['start'])
async def cmd_start(msg: types.Message):
    user = open('users/'+msg.chat.username+'.txt', 'w')
    user.write(str(msg.from_user.id))
    user.close()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    time_now = datetime.now().strftime('%H:%M')  #######
    print(msg.chat.username + " начал использовать бота в [" + time_now + "]")  #######
    time_now = datetime.now().strftime('%H:%M')
    test = open('logs.txt', 'a')
    test.write("\n" + msg.chat.username + " начал использовать бота в [" + time_now + "]")
    test.close()
    buttons = ["Замотивируй меня", "Помоги", "Уведомления"]
    keyboard.add(*buttons)
    await msg.answer(
        "Привет, <b>" + msg.chat.username + '</b>!\nЯ мотивирующий бот!\nНапиши "<u>Замотивируй меня</u>", и я выдам тебе мотивашку!',
        parse_mode="HTML", reply_markup=keyboard)


@dp.message_handler(Text(equals="Замотивируй меня"))
async def with_puree(msg: types.Message):
    time_now = datetime.now().strftime('%H:%M')  #######
    print("[" + time_now + "] " + msg.chat.username + ": " + msg.text)
    test = open('logs.txt', 'a')  ######
    test.write("\n[" + time_now + "] " + msg.chat.username + ": " + msg.text)  ########
    test.close()  #############
    user = open('users/' + msg.chat.username + '.txt', 'w')
    user.write(str(msg.from_user.id))
    user.close()
    files = os.listdir(directory)
    #print(len(files))
    num = str(random.randint(0, len(files)))
    photo = InputFile(path_or_bytesio='assets/' + num + '.jpg')
    await bot.send_photo(chat_id=msg.chat.id, photo=photo)


@dp.message_handler(Text(equals="Помоги"))
async def process_help_command(msg: types.Message):
    time_now = datetime.now().strftime('%H:%M')  ######
    print("[" + time_now + "] " + msg.chat.username + ": " + msg.text)
    test = open('logs.txt', 'a')  ######
    test.write("\n[" + time_now + "] " + msg.chat.username + ": " + msg.text)  ######
    test.close()  ##############
    await msg.reply('Напиши "<u>Замотивируй меня</u>", и я выдам тебе мотивашку!\nЕсли хочешь получать уведомления от меня, напиши "<u>Уведомления</u>"', parse_mode="HTML")

@dp.message_handler(commands="send")  ##################
async def echo_message(msg: types.Message):
    #time_now = datetime.now().strftime('%H:%M')  ######
    if msg.from_user.id == adminId and msg.chat.username == adminName:
        arg = msg.get_args()
        text = arg.split(" ")
        string = ''
        userN = text[0]
        #print(text)
        text.pop(0)
        for el in text:
            string += el + ' '
        file = open('users/'+str(userN)+'.txt')
        dataID = file.read()
        file.close()
    #print(dataID)
        await bot.send_message(chat_id=dataID, text = string)
        await bot.send_message(chat_id=msg.from_user.id, text = 'Сообщение - "'+string+'", доставлено пользователю ' + userN)
    else:
        await bot.send_message(chat_id=msg.from_user.id, text="Ты черт, а не админ!")

@dp.message_handler(commands="photoTo")  ##################
async def echo_message(msg: types.Message):
    if msg.from_user.id == adminId and msg.chat.username == adminName:
        arg = msg.get_args()
        text = arg.split(" ")
        string = ''
        userN = text[0]
        #print(text)
        file = open('users/'+str(userN)+'.txt')
        dataID = file.read()
        file.close()
        files = os.listdir(directory)
        #print(len(files))
        num = str(random.randint(0, len(files)))
        photo = InputFile(path_or_bytesio='assets/' + num + '.jpg')
        await bot.send_photo(chat_id=dataID, photo=photo)
        await bot.send_message(chat_id=dataID, text="Тебе картинка от админа!")
        await bot.send_message(chat_id=msg.from_user.id, text='Картинка доставлена пользователю ' + userN)
    else:
        await bot.send_message(chat_id=msg.from_user.id, text="Ты черт, а не админ!")
#############

@dp.message_handler(commands="all")  ##################
async def echo_message(msg: types.Message):
    #time_now = datetime.now().strftime('%H:%M')  ######
    if msg.from_user.id == adminId and msg.chat.username == adminName:
        string = str(msg.get_args())
        with open('users.txt', 'r') as filehandle:
            filecontents = filehandle.readlines()
        for line in filecontents:
            current_place = line[:-1]
            users.append(current_place)
        for idUser in users:
            await bot.send_message(chat_id=int(idUser), text=string)
        await bot.send_message(chat_id=adminId, text = 'Сообщения успешно доставлены пользователям!')
    else:
        await bot.send_message(chat_id=msg.from_user.id, text="Ты не админ!")
@dp.message_handler(Text(equals="Уведомления"))
async def process_help_command(msg: types.Message):
    if str(msg.from_user.id) not in str(users):
        users.append(msg.from_user.id)
        print(users)
        file = open("users.txt","a")
        file.write(str(msg.from_user.id)+"\n")
        file.close()
        await bot.send_message(chat_id=msg.from_user.id, text="Ты успешно добавлен!")
    else:
        await bot.send_message(chat_id=msg.from_user.id, text="Ты уже добавлен!")
    #############
@dp.message_handler()  ##################
async def echo_message(msg: types.Message):
    time_now = datetime.now().strftime('%H:%M')
    print("[" + time_now + "] " + msg.chat.username + ": " + msg.text)
    test = open('logs.txt', 'a')
    test.write("\n[" + time_now + "] " + msg.chat.username + ": " + msg.text)
    test.close()

async def on_startup():
    with open('users.txt', 'r') as filehandle:
        filecontents = filehandle.readlines()
    for line in filecontents:
        current_place = line[:-1]
        users.append(current_place)
    #for idUser in users:
        #await bot.send_message(chat_id=int(idUser), text='Бот запущен')

if __name__ == '__main__':
    executor.start(dp, on_startup())
    executor.start_polling(dp)