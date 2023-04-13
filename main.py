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
adminName = ADMIN_NAME
adminId = ADMIN_ID


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
    buttons = ["Замотивируй меня", "Помоги"]
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
    num = str(random.randint(0, 62))
    photo = InputFile(path_or_bytesio='assets/' + num + '.jpg')
    await bot.send_photo(chat_id=msg.chat.id, photo=photo)


@dp.message_handler(Text(equals="Помоги"))
async def process_help_command(msg: types.Message):
    time_now = datetime.now().strftime('%H:%M')  ######
    print("[" + time_now + "] " + msg.chat.username + ": " + msg.text)
    test = open('logs.txt', 'a')  ######
    test.write("\n[" + time_now + "] " + msg.chat.username + ": " + msg.text)  ######
    test.close()  ##############
    await msg.reply('Напиши "<u>Замотивируй меня</u>", и я выдам тебе мотивашку!', parse_mode="HTML")


@dp.message_handler(Text(equals="Список"))  ##################
async def echo_message(msg: types.Message):
    time_now = datetime.now().strftime('%H:%M')  ######
    print("Пользователь " + msg.chat.username + "(" + str(
        msg.from_user.id) + ") обратился ко мне за списком в [" + time_now + "]")
    if msg.from_user.id == 933846611 and msg.chat.username == adminName:
        await msg.reply(
            'Приветствую, <b> Г-н Администратор!</b>\nВот список пользователей, использовавших меня: ' + str(listUser),
            parse_mode="HTML")
    else:
        await msg.reply('<b>Ты не администратор этого бота! Тебе нельзя использовать эту команду!</b>',
                        parse_mode="HTML")

@dp.message_handler(commands="send")  ##################
async def echo_message(msg: types.Message):
    #time_now = datetime.now().strftime('%H:%M')  ######
    if msg.from_user.id == 933846611 and msg.chat.username == adminName:
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
    else:
        await bot.send_message(chat_id=msg.from_user.id, text="Ты черт, а не админ!")

#############

@dp.message_handler()  ##################
async def echo_message(msg: types.Message):
    time_now = datetime.now().strftime('%H:%M')
    print("[" + time_now + "] " + msg.chat.username + ": " + msg.text)
    test = open('logs.txt', 'a')
    test.write("\n[" + time_now + "] " + msg.chat.username + ": " + msg.text)
    test.close()

    #############

if __name__ == '__main__':
    executor.start_polling(dp)
