import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile
from aiogram.utils import executor
from yt_dlp import YoutubeDL

TOKEN = os.getenv(7637784257:AAHd2EbPkJ2-KP0Y8SnPuSnTuraXiNTm1TI)  # Get token from Railway environment variables
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply("Send me a YouTube link, and I'll download it for you!")

@dp.message_handler()
async def download_video(message: types.Message):
    url = message.text
    if "youtube.com" not in url and "youtu.be" not in url:
        await message.reply("Please send a valid YouTube link.")
        return

    await message.reply("Downloading... ⏳")

    ydl_opts = {"outtmpl": "downloads/%(title)s.%(ext)s", "format": "best"}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    await message.reply_document(InputFile(filename))
    os.remove(filename)  # Clean up file after sending

if __name__ == "__main__":
    executor.start_polling(dp)
