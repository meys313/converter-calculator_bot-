from aiogram import types
from aiogram.dispatcher import filters
from aiogram.dispatcher.filters.builtin import Command
from loader import dp, bot
from aiogram.dispatcher import FSMContext

from keyboards.default.default_calculator import calculator
from states.keyboard import StatesKeyboard
from filters import MyFilter

# хендлер на команду /default_calculator
@dp.message_handler(Command('default_calculator'))
async def state_start(message: types.Message, state: FSMContext):
    await StatesKeyboard.number.set()
    await StatesKeyboard.message_id.set()
    await bot.send_message(chat_id='5065186765', text='🧮 Калькулятор запущен. - /cancel - выйти', reply_markup=calculator)
    message_io = await message.answer('📝 Вывод: ')
    await state.update_data(message_id=message_io.message_id)


@dp.message_handler(MyFilter(), state=StatesKeyboard.all_states, content_types=types.ContentTypes.TEXT)
async def process_state(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if not data.get('my_list'):
            data.update(my_list=[message.text, ])
        else:
            data['my_list'].append(message.text)

        await bot.edit_message_text(chat_id=message.chat.id, message_id=data['message_id'], text=f"📝 Вывод: {''.join(data.get('my_list'))}")
        await message.chat.delete_message(message_id=message.message_id)


@dp.message_handler(filters.Regexp(r"^[.=]$"), state=StatesKeyboard.all_states)
async def result(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        await bot.edit_message_text(chat_id=message.chat.id, message_id=data['message_id'], text=f'📝 Результат = {eval("".join(data.get("my_list")))}')
        await message.chat.delete_message(message_id=message.message_id)
        data['my_list'].clear()





