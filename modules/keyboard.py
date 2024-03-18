from aiogram import types

Button = types.KeyboardButton
default_buttons = [
    [
    Button(text="<<"),
    Button(text="отправить книгу"),
    Button(text=">>")
    ]
]
default_keyboard = types.ReplyKeyboardMarkup(
    keyboard=default_buttons,
    resize_keyboard=True,
    input_field_placeholder="куда вы хотите попасть?"
)


admin_buttons = [
    [
    types.KeyboardButton(text="-5"),
    types.KeyboardButton(text="выход"),
    types.KeyboardButton(text="+5"),
    ],
    [
    types.KeyboardButton(text="<<"),
    types.KeyboardButton(text=">>"),
    ],
    ]
admin_keyboard = types.ReplyKeyboardMarkup(
    keyboard=admin_buttons,
    resize_keyboard=True,
    input_field_placeholder="куда вы хотите попасть?"
    )

