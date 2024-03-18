import asyncio
import logging
import sys
from os import access, getenv
import json

from db.database_utils import DB

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.filters.command import Command

load_dotenv()
TOKEN = getenv("TOKEN")
#print(TOKEN)

dp = Dispatcher()
db = DB("./db/users.db")


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("Доброго времени суток, дорогой читатель, это книжный бот!")
    db.create_new_user(message.chat.id)
    kb = [
        [
            types.KeyboardButton(text="новая глава"),
            types.KeyboardButton(text="отправить книгу"),
            types.KeyboardButton(text="предыдущая глава"),
        ],
    ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="куда вы хотите попасть?"
    )
    await message.answer(f"твоя глава {db.get_status(message.chat.id)}", reply_markup=keyboard)

def read_book(id: int):
    status = db.get_status(id)
    with open(f"./books/chapter/chapter_{status}.txt", 'r', encoding='utf-8') as file:
        book = file.read()
    return book

@dp.message()
async def admin(message: types.Message):
    global temp_super_user
    global admin_json
    global accessed

    if message.text == "admin":
        temp_super_user = message.chat.id
        accessed = False
        await message.answer("вы не отправили пароль")

    elif message.text == "отправить книгу":
        #status = db.get_status(message.chat.id)
        chapter = read_book(message.chat.id)
        await message.answer(chapter)

    elif message.chat.id == temp_super_user:
        if message.text == admin_json['password'] and not accessed:
            accessed = True
            kb = [
                    [
                    types.KeyboardButton(text="новая глава"),
                    types.KeyboardButton(text="предыдущая глава")
                    ],
                ]
            keyboard = types.ReplyKeyboardMarkup(
                keyboard=kb,
                resize_keyboard=True,
                input_field_placeholder="куда вы хотите попасть?"
            )
            await message.answer("теперь у вас есть доступ к главам", reply_markup=keyboard)

        elif message.text == "новая глава" and accessed and temp_super_user == message.chat.id:
            await message.answer("новая страница")
            admin_json["max_chapter"] += 1;

            with open("./db/admin_json", 'w') as file:
                json_object = json.dumps(admin_json, indent=4)
                file.write(json_object)
            await message.answer(f"теперь ваша максимальная глава для прочтения {admin_json['max_chapter']}")


        elif message.text == "предыдущая глава" and access and temp_super_user == message.chat.id:
            if admin_json["max_chapter"] > 1:
                admin_json["max_chapter"] -= 1

                with open("./db/admin.json", 'w') as file:
                    json_object = json.dumps(admin_json, indent=4)
                    file.write(json_object)
                await message.answer(f"теперь ваша максимальная глава для прочтения {admin_json['max_chapter']}")
            else:
                await message.answer("ваша глава уже 1")
    elif message.text == "выход" and message.chat.id == temp_super_user:
        access = False
    elif message.text == "предыдущая глава":
        status = db.get_status(message.chat.id)
        if status > 1:
            db.change_prev_step(message.chat.id)
            await message.answer(f"теперь ваша глава {status - 1}")
        else:
            await message.answer("ваша глава уже 1")

    elif message.text == "новая глава":
        status = db.get_status(message.chat.id)
        if status <= admin_json["max_chapter"]:
            db.change_next_step(message.chat.id)
            await message.answer(f"теперь ваша глава {status + 1}")
        else:
            await message.answer("извините, но вы еще не прочитали эту главу")

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
    with open("./db/admin.json", 'r') as file:
        admin_json = json.load(file)

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())