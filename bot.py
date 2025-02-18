from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message
from imei import validate_imei, get_imei_info

from config_reader import config

bot = Bot(token=config.bot_token.get_secret_value(),
          default=DefaultBotProperties(
              parse_mode=ParseMode.HTML

          )
          )

dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(f"Здравствуйте {message.from_user.full_name}! Введите IMEI устройства.")


@dp.message(Command("help"))
async def start(message: Message):
    await message.answer(
        f"Бот предоставляет информацию об устройстве, используя API сервиса https://imeicheck.net/, по его IMEI.")


@dp.message(F.text)
async def imei(message: Message):
    if validate_imei(message.text):
        imei_data = await get_imei_info(message.text, config.api_key.get_secret_value())

        if imei_data["status"] == "successful":
            await message.answer(f"Устройство:{imei_data["properties"]["deviceName"]}\n"
                                 f"IMEI: {imei_data["properties"]["imei"]}\n"
                                 f"IMEI2: {imei_data["properties"]["imei2"]}")
        else:
            await message.answer("Не удалось получить данные, повторите попытку.")
    else:
        await message.answer("IMEI не валиден, проверьте правильность введенных данных")


async def start_bot():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

