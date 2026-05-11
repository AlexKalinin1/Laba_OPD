import logging
import asyncio
import random
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

logging.basicConfig(level=logging.INFO)

bot = Bot(token="8677219699:AAEAcXIJj8LWg6fqK9JcwJukiaalH2b_rKY")
dp = Dispatcher()

MOTIVATION_IMAGES = [
    "https://images.unsplash.com/photo-1490730141103-6cac27aaab94?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1470770903676-69b98201ea1c?auto=format&fit=crop&w=800&q=80"
]

MOTIVATION_TEXTS = [
    "У тебя всё получится!",
    "Не сдавайся!",
    "Иди к своей цели!",
    "Каждый день — новый шанс!",
    "Ты сильнее, чем думаешь!"
]


def get_random_motivation():
    image = random.choice(MOTIVATION_IMAGES)
    text = random.choice(MOTIVATION_TEXTS)
    return image, text


def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Получить мотивашку")]
        ],
        resize_keyboard=True
    )
    return keyboard


@dp.message(Command('start', 'help'))
async def process_start_command(message: Message):
    await message.reply(
        "Бот мотивашек.\n"
        "Нажми кнопку или используй команду /motivate",
        reply_markup=get_main_keyboard()
    )


@dp.message(Command('motivate'))
async def process_motivate_command(message: Message):
    image, text = get_random_motivation()
    await message.answer_photo(photo=image, caption=text)


@dp.message(Command('list'))
async def process_list_command(message: Message):
    text = "Список мотивационных фраз:\n\n"
    for i, phrase in enumerate(MOTIVATION_TEXTS, 1):
        text += f"{i}. {phrase}\n"
    await message.reply(text)


@dp.message()
async def process_any_message(message: Message):
    if message.text == "Получить мотивашку":
        image, text = get_random_motivation()
        await message.answer_photo(photo=image, caption=text)
    else:
        await message.reply("Используй /start или кнопку.")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())