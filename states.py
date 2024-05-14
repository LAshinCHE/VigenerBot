from aiogram.fsm.state import StatesGroup, State

class CodeState(StatesGroup):
    encode_state = State()
    decode_text_state = State()
    decrypt_selected_state = State()
    new_key_state = State()