import logging

from aiogram import types, F, Router
from aiogram.types import InlineKeyboardButton, Message, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, callback_query
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder


from aiogram import flags
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter

import utils
from states import CodeState

router = Router()

encrypted_message_storage=[]

key_word = "SKVAZIMABZBZ"

buttons = [
    [InlineKeyboardButton(text="encrypt", callback_data=f"encrypt_callback"),
    InlineKeyboardButton(text="decrypt", callback_data=f"decrypt_text_callback"),
    InlineKeyboardButton(text="decrypt encrypted message", callback_data=f"decode_selected_callback")],
    [InlineKeyboardButton(text="chose key word", callback_data=f"set_key")]
]

shifreVal = {}

buttons = InlineKeyboardMarkup(inline_keyboard=buttons)


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(f"Приветствую, {msg.from_user.full_name}.\n  Текущее ключевое слово: {key_word}", reply_markup=buttons)

@router.message(Command("menue"))
async def generate_menue(msg: Message):
    await msg.answer("Меню:", reply_markup=buttons)

@router.callback_query(F.data == "encrypt_callback")
async def encrypt_callback(callback: types.CallbackQuery, state : FSMContext):
    logging.info("STARTING ENCODE MESSAGE")
    await state.set_state(CodeState.encode_state)
    await callback.message.edit_text("Напишите слово, которое хотели бы зашифровать:")


@router.callback_query(F.data == "decrypt_text_callback")
async def decrypt_text_callback(callback: types.CallbackQuery, state : FSMContext):
    await state.set_state(CodeState.decode_text_state)
    await callback.message.edit_text("Напишите слово к которому вы хотите применить алгоритм дешифровки:")


@router.callback_query(F.data == "set_key")
async def set_key(callback: types.CallbackQuery, state : FSMContext):
    await state.set_state(CodeState.new_key_state)
    await callback.message.edit_text("Напишите слово, которое будет ключом:")


@router.message(CodeState.encode_state)
@flags.chat_action("typing")
async def encode_state(msg: Message, state: FSMContext):
    query = msg.text
    mesg = await msg.answer("Ждите ответа на запрос")
    res, shifre = utils.EncodeText(query, key_word)
    logging.info(f"CODED MESSAGE: {res}, SHIFRE: {shifre}")
    shifreVal[res] = shifre
    if len(res) == 0:
        return await mesg.edit_text("Ошибка при зашифровывания сообщения")
    encrypted_message_storage.append(res)
    await mesg.edit_text(res, reply_markup=buttons)
   


@router.callback_query(F.data == "decode_selected_callback")
async def decrypt_text_callback(callback: types.CallbackQuery, state : FSMContext):
    if len(encrypted_message_storage) > 0:
        await state.set_state(CodeState.decrypt_selected_state)
        message = ""
        for i in range(len(encrypted_message_storage)):
            word = encrypted_message_storage[i]
            if i == 0:
                message += ": " + word + " : "
            else:
                message += word + " : "
        await callback.message.edit_text("Выберете слово которое вы хотите расшифровать из списка:\n" + message)
    else:
        await callback.message.edit_text("Список зашифрованных сообщений пуст.\nДля начала зашифруйте сообщение", reply_markup=buttons)


            
@router.message(CodeState.new_key_state)
@flags.chat_action("typing")
async def new_key_set(msg: Message, state: FSMContext):
    query = msg.text
    mesg = await msg.answer("Ждите ответа на запрос")
    if len(query) != 0:
        global key_word
        key_word = query 
        await mesg.edit_text(key_word, reply_markup=buttons)
    else:
        await  mesg.edit_text("Невозможно установить слово нулевой длины", reply_markup=buttons)



@router.message(CodeState.decode_text_state)
@flags.chat_action("typing")
async def encode_text(msg: Message, state: FSMContext):
    query = msg.text
    mesg = await msg.answer("Ждите ответа на запрос")
    res = utils.DecodeText(shifreVal[query], key_word)
    print("res=",res)
    if len(res) == 0:
        return await mesg.edit_text("Ошибка при расшифровки сообщения")
    await mesg.edit_text(res, reply_markup=buttons)


@router.message(CodeState.decrypt_selected_state)
@flags.chat_action("typing")
async def decode_selected_message(msg: Message, state: FSMContext):
    query = msg.text
    mesg = await msg.answer("Ждите ответа на запрос")
    if query in encrypted_message_storage:
        res = utils.DecodeText(query)
        if len(res) == 0:
            return await mesg.edit_text("Ошибка при расшифровки сообщения")
        encrypted_message_storage.remove(query)
        await mesg.edit_text(res, reply_markup=buttons)
    else:
        await mesg.edit_text("Данного слова нет в списке", reply_markup=buttons)