from aiogram import Bot, Dispatcher, types
from aiogram.client import bot
from aiogram.fsm import storage
from aiogram.fsm.storage.memory import MemoryStorage

API_TOKEN = 'AAFYhQuuQsVKisCcszn2K_87IZuEjwVBQdQ'

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Welcome! You will receive notifications for new messages.")

