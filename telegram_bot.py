from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

API_TOKEN = 'Введите токен'
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

user_chat_ids = set()

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    user_chat_ids.add(message.chat.id)  # Сохраняем chat_id пользователя
    await message.reply("Добро пожаловать!")

async def notify_new_message(new_message: str):
    for chat_id in user_chat_ids:
        try:
            await bot.send_message(chat_id, f'Новое сообщение: {new_message}')
        except Exception as e:
            print(f"Не удалось отправить сообщение пользователю {chat_id}: {e}")

async def start_bot():
    await dp.start_polling(bot)
