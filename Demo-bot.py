import os
import logging
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiohttp import web

# Сюда вставляется токен, который клиент получит от своего BotFather
TOKEN = "ТВОЙ_ТОКЕН_ПРОБНОГО_БОТА"
ADMIN_USERNAME = "ТвойЮзернейм"  # Куда клиент будет писать по вопросам заказа

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_main_menu():
    b = InlineKeyboardBuilder()
    b.button(text="📋 О наших услугах", callback_data="services")
    b.button(text="💼 Портфолио работ", callback_data="portfolio")
    b.button(text="📞 Связаться с менеджером", url=f"https://t.me/{ADMIN_USERNAME}")
    b.adjust(1)
    return b.as_markup()

@dp.message(Command("start"))
async def cmd_start(msg: types.Message):
    await msg.answer(
        "👋 Здравствуйте! Добро пожаловать в нашу компанию.\n\n"
        "Этот бот создан для автоматизации вашего бизнеса. Выберите интересующий раздел:",
        reply_markup=get_main_menu()
    )

@dp.callback_query(F.data == "services")
async def show_services(c: types.CallbackQuery):
    b = InlineKeyboardBuilder()
    b.button(text="⬅️ Назад в меню", callback_data="back_home")
    b.adjust(1)
    await c.message.edit_text(
        "📋 **Наши основные услуги:**\n\n"
        "1. Разработка Telegram-ботов любой сложности.\n"
        "2. Интеграция с CRM и платежными системами.\n"
        "3. Техническая поддержка 24/7.",
        reply_markup=b.as_markup()
    )
    await c.answer()

@dp.callback_query(F.data == "portfolio")
async def show_portfolio(c: types.CallbackQuery):
    b = InlineKeyboardBuilder()
    b.button(text="⬅️ Назад в меню", callback_data="back_home")
    b.adjust(1)
    await c.message.edit_text(
        "💼 **Портфолио:**\n\n"
        "• Бот-магазин одежды\n"
        "• Бот для записи в барбершоп\n"
        "• Интерактивный бот-знакомств",
        reply_markup=b.as_markup()
    )
    await c.answer()

@dp.callback_query(F.data == "back_home")
async def back_home(c: types.CallbackQuery):
    await c.message.edit_text(
        "Главное меню. Выберите интересующий раздел:",
        reply_markup=get_main_menu()
    )
    await c.answer()

async def handle(request):
    return web.Response(text="Commercial Bot is running!")

app = web.Application()
app.router.add_get("/", handle)

if __name__ == "__main__":
    # Локальный запуск или через polling для теста
    async def main():
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    
    # Для работы веб-сервера на Render/Heroku:
    asyncio.run(main())
