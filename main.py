import asyncio
import logging
import sys
import os 
import json

from db.database_utils import DB
import modules.keyboard as kbs
from db.table_exec import create_db

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.filters.command import Command

load_dotenv()
TOKEN = os.getenv("TOKEN")
#print(TOKEN)

dp = Dispatcher()

DB_URL = os.path.abspath("./db/users.db")
db = DB(DB_URL)

def read_book(id: int):
    status = db.get_status(id)
    with open(os.path.abspath(f"./books/chapter/chapter_{status}.txt"), 'r', encoding='utf-8') as file:
        book = file.read()
    return book

def update_admin_json():
    global admin_json
    global pass_admin
    with open(path_admin, "w") as file:
        json_object = json.dumps(admin_json, indent=4)
        file.write(json_object)

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("Доброго времени суток, дорогой читатель, это книжный бот!")
    db.create_new_user(message.chat.id)

    await message.answer(f"Сейчас вы находитесь на {db.get_status(message.chat.id)} главе.", reply_markup=kbs.default_keyboard)

@dp.message(Command("get_chapter"))
async def get_chapter(message: Message) -> None:
    await message.answer(f"Сейчас вы находитесь на {db.get_status(message.chat.id)} главе.")

@dp.message(Command("get_max_chapter"))
async def get_max_chapter(message: Message) -> None:
    global admin_json
    await message.answer(f"максимальная глава для прочтения - {admin_json['max_chapter']}")

@dp.message()
async def admin(message: types.Message) -> None:
    global temp_super_user
    global admin_json
    global accessed

    if message.text == "admin":
        temp_super_user = message.chat.id
        accessed = False
        await message.answer("Вам нужно отправить пароль или выйти", reply_markup=kbs.exit_keyboard)

    elif message.text == "отправить книгу":
        #status = db.get_status(message.chat.id)
        chapter = read_book(message.chat.id)
        await message.answer(chapter)

    elif message.chat.id == temp_super_user:
        if message.text == admin_json['password'] and not accessed:
            accessed = True
            await message.answer("теперь у вас есть доступ к главам", reply_markup=kbs.admin_keyboard)
        elif message.text == "выйти" and message.chat.id == temp_super_user:
            accessed = False
            temp_super_user = 0
            await message.answer("Вы вышли", reply_markup=kbs.default_keyboard)
        elif accessed and temp_super_user == message.chat.id:

            if message.text == ">>":
                #await message.answer("новая страница")
                admin_json["max_chapter"] += 1;

                update_admin_json() 
                await message.answer(f"теперь максимальная глава для прочтения - {admin_json['max_chapter']}")


            elif message.text == "<<":
                if admin_json["max_chapter"] > 1:
                    admin_json["max_chapter"] -= 1

                    update_admin_json()
                    await message.answer(f"теперь максимальная глава для прочтения - {admin_json['max_chapter']}")
                else:
                    await message.answer("Вы уже на 1 главе")

            elif message.text == "+5":
                admin_json["max_chapter"] += 5
                update_admin_json()
                await message.answer(f"теперь максимальная глава для прочтения - {admin_json['max_chapter']}")

            elif message.text == "-5":
                if admin_json["max_chapter"] > 5:
                    admin_json["max_chapter"] -= 5
                    update_admin_json()
                    await message.answer(f"теперь максимальная глава для прочтения - {admin_json['max_chapter']}")
                else:
                    admin_json["max_chapter"] = 1
                    await message.answer("Вы уже на 1 главе")
            elif message.text == "выйти":
                accessed = False
                temp_super_user = 0
                await message.answer("Вы вышли", reply_markup=kbs.default_keyboard)
        else:
            await message.answer("Вам нужно отправить пароль или выйти", reply_markup=kbs.exit_keyboard)


    elif message.text == "<<":
        status = db.get_status(message.chat.id)
        if status > 1:
            db.change_prev_step(message.chat.id)
            await message.answer(f"Сейчас вы находитесь на {status - 1} главе.")
        else:
            await message.answer("Вы уже на 1 главе")

    elif message.text == ">>":
        status = db.get_status(message.chat.id)
        if status < admin_json["max_chapter"]:
            db.change_next_step(message.chat.id)
            await message.answer(f"Сейчас вы находитесь на {status + 1} главе.")
        else:
            await message.answer("извините, но вы еще не прочитали эту главу")
    elif message.text == "выйти":
        await message.answer("Вы вышли", reply_markup=kbs.default_keyboard)
    else:
        await message.answer("Извините, я не могу вас понять!")

async def main() -> None:
    if TOKEN is not None:
        Token = str(TOKEN)
    else:
        print("TOKEN is not in .env file!")
        quit(1)
    bot = Bot(Token, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    temp_super_user = 0
    accessed = False
    admin_json = {}
    path_admin = os.path.abspath("./db/admin.json")
    if os.path.isfile(path_admin):
        with open(path_admin, 'r') as file:
            admin_json = json.load(file)
    else:
        logging.log(level=logging.WARN, msg="admin_json is not in file")

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
