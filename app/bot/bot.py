# import asyncio
# import logging
# import sys
#
# from aiogram import Bot, Dispatcher, Router, F
# from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
# from aiogram.filters import Command
# import httpx
# from sqlalchemy import select
#
# import app.config
# from app.crud import get_product_by_article
# from app.database import async_session
# from app.models import Product
#
# bot = Bot(token=app.config.settings.BOT_TOKEN)
# router = Router()
# dp = Dispatcher()
# dp.include_router(router)
#
#
# def get_product_keyboard():
#     button = InlineKeyboardButton(text="Get Product Data", callback_data="get_data")
#     return InlineKeyboardMarkup(inline_keyboard=[[button]])
#
#
# @router.message(Command("start"))
# async def start(message: Message):
#     await message.answer(
#         "Click the button below to get product data.",
#         reply_markup=get_product_keyboard(),
#     )
#
#
# @router.callback_query(F.data == "get_data")
# async def process_get_data(callback_query: CallbackQuery):
#     await callback_query.message.answer("Send the product article:")
#
#     @router.message()
#     async def fetch_data(message: Message):
#         article = message.text
#         await callback_query.answer()
#         async with async_session() as session:
#             product = await get_product_by_article(session, article)
#             if product:
#                 await message.answer(
#                     f"Product with {product.article:}\n"
#                     f"Name: {product.name}\n"
#                     f"Price: {product.price}\n"
#                     f"Rating: {product.rating}\n"
#                     f"Stock: {product.stock}"
#                 )
#             else:
#                 await message.answer("Product not found.")
#
#
# async def main() -> None:
#     await dp.start_polling(bot)
#
#
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO, stream=sys.stdout)
#     asyncio.run(main())
import asyncio
import logging
import sys

import aiohttp
from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

import app.config
from app.schemas import ProductSchema

bot = Bot(token=app.config.settings.BOT_TOKEN)
router = Router()
dp = Dispatcher()
dp.include_router(router)


def get_product_keyboard():
    button = KeyboardButton(text="Get Product Data")
    return ReplyKeyboardMarkup(keyboard=[[button]], resize_keyboard=True)


@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Click the button below to get product data.",
        reply_markup=get_product_keyboard(),
    )


@router.message(F.text == "Get Product Data")
async def process_get_data(message: Message):
    await message.answer("Send the product article:")

    @router.message()
    async def fetch_data(article_message: Message):
        article = article_message.text
        async with aiohttp.ClientSession() as session:
            URL = f'http://localhost:8000/api/v1/products/?artikul={article}'
            try:
                async with session.post(URL) as response:
                    if response.status == 200:
                        product_data = await response.json()
                        if product_data:
                            product = ProductSchema(**product_data)
                            await article_message.answer(
                                f"Article: {product.article}\n"
                                f"Name: {product.name}\n"
                                f"Price: {product.price}\n"
                                f"Rating: {product.rating}\n"
                                f"Stock: {product.stock}"
                            )
                        else:
                            await article_message.answer("Product not found.")
                    else:
                        await article_message.answer(f"Error: Request failed with status {response.status}")
            except Exception as e:
                await article_message.answer(f"An error occurred: {str(e)}")

        # async with async_session() as session:
        #     product = await get_product_by_article(session, article)
        #     if product:
        #         await article_message.answer(
        #             f"Article: {product.article}\n"
        #             f"Name: {product.name}\n"
        #             f"Price: {product.price}\n"
        #             f"Rating: {product.rating}\n"
        #             f"Stock: {product.stock}"
        #         )
        #     else:
        #         await article_message.answer("Product not found.")


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
