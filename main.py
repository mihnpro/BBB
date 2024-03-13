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
    await message.answer("Hello, this is book bot for lessons!")
    db.create_new_user(message.chat.id)
    kb = [
        [
            types.KeyboardButton(text="New chapter"),
            types.KeyboardButton(text="send_book"),
            types.KeyboardButton(text="Previos chapter"),
        ],
    ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="which way you want to go"
    )
    await message.answer(f"your page is {db.get_status(message.chat.id)}", reply_markup=keyboard)

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
        await message.answer("now send me a password")

    elif message.text == "send_book":
        #status = db.get_status(message.chat.id)
        chapter = read_book(message.chat.id)
        await message.answer(chapter)

    elif message.chat.id == temp_super_user:
        if message.text == admin_json['password'] and not accessed:
            accessed = True
            kb = [
                    [
                    types.KeyboardButton(text="New chapter"),
                    types.KeyboardButton(text="Previos chapter")
                    ],
                ]
            keyboard = types.ReplyKeyboardMarkup(
                keyboard=kb,
                resize_keyboard=True,
                input_field_placeholder="which way you want to go"
            )
            await message.answer("now you can modify accses to chapters", reply_markup=keyboard)

        elif message.text == "New chapter" and accessed and temp_super_user == message.chat.id:
            await message.answer("new page")
            admin_json["max_chapter"] += 1;

            with open("./db/admin_json", 'w') as file:
                json_object = json.dumps(admin_json, indent=4)
                file.write(json_object)
            await message.answer(f"Now max chapter is {admin_json['max_chapter']}")


        elif message.text == "Previos chapter" and access and temp_super_user == message.chat.id:
            if admin_json["max_chapter"] > 1:
                admin_json["max_chapter"] -= 1

                with open("./db/admin.json", 'w') as file:
                    json_object = json.dumps(admin_json, indent=4)
                    file.write(json_object)
                await message.answer(f"Now max chapter is {admin_json['max_chapter']}")
            else:
                await message.answer("chapter is already 1")
    elif message.text == "exit" and message.chat.id == temp_super_user:
        access = False
    elif message.text == "Previos chapter":
        status = db.get_status(message.chat.id)
        if status > 1:
            db.change_prev_step(message.chat.id)
            await message.answer(f"now your page is {status - 1}")
        else:
            await message.answer("page is already 1")

    elif message.text == "New chapter":
        status = db.get_status(message.chat.id)
        if status <= admin_json["max_chapter"]:
            db.change_next_step(message.chat.id)
            await message.answer(f"now your page is {status + 1}")
        else:
            await message.answer("sorry, but admin think that you need to just read this page!")

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
