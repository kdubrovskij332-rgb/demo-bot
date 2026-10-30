import os
import logging
import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiohttp import web

TOKEN = "9074013397:AAGT4oqK1RwH2_xw9IP5I4sUMacLSCMqtO8"
ADMIN_USERNAME = "GoodBus1nesBot"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

def init_db():
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE,
            username TEXT,
            full_name TEXT,
            joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

def get_main_menu():
    b = InlineKeyboardBuilder()
    b.button(text="🌐 Сетевые услуги и IT", callback_data="services")
    b.button(text="💼 Портфолио проектов", callback_data="portfolio")
    b.button(text="💳 Оплата и тарифы", callback_data="payment")
    b.button(text="📞 Связаться со специалистом", url=f"https://t.me/{ADMIN_USERNAME}")
    b.adjust(1)
    return b.as_markup()

def get_back_menu():
    b = InlineKeyboardBuilder()
    b.button(text="⬅️ Вернуться в главное меню", callback_data="back_home")
    b.adjust(1)
    return b.as_markup()

@dp.message(Command("start"))
async def cmd_start(msg: types.Message):
    try:
        conn = sqlite3.connect("bot_database.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO clients (telegram_id, username, full_name) VALUES (?, ?, ?)",
            (msg.from_user.id, msg.from_user.username or "No", msg.from_user.full_name or "No")
        )
        conn.commit()
        conn.close()
    except Exception as e:
        logging.error(e)

    text = (
        "👋 Добро пожаловать в профессиональный IT-сервис!\n\n"
        "Мы специализируемся на проектировании и настройке сетей.\n\n"
        "Выберите интересующий раздел:"
    )
    await msg.answer(text, reply_markup=get_main_menu())

@dp.callback_query(F.data == "services")
async def show_services(c: types.CallbackQuery):
    text = (
        "🌐 Наши сетевые решения:\n\n"
        "1. Локальные и глобальные сети (LAN/WAN, VPN)\n"
        "2. Настройка оборудования (MikroTik, Cisco)\n"
        "3. Системное администрирование и Active Directory"
    )
    await c.message.edit_text(text, reply_markup=get_back_menu())
    await c.answer()

@dp.callback_query(F.data == "portfolio")
async def show_portfolio(c: types.CallbackQuery):
    text = (
        "💼 Примеры проектов:\n\n"
        "• СКС для офиса на 150 рабочих мест\n"
        "• Настройка бесшовного Wi-Fi и VLAN\n"
        "• Защищенные шлюзы и видеонаблюдение"
    )
    await c.message.edit_text(text, reply_markup=get_back_menu())
    await c.answer()

@dp.callback_query(F.data == "payment")
async def show_payment(c: types.CallbackQuery):
    text = (
        "💳 Способы оплаты:\n\n"
        "• Банковская карта\n"
        "• Безналичный расчет для юридических лиц\n"
        "• USDT / Криптовалюта"
    )
    b = InlineKeyboardBuilder()
    b.button(text="📞 Связаться для заказа", url=f"https://t.me/{ADMIN_USERNAME}")
    b.button(text="⬅️ Вернуться в меню", callback_data="back_home")
    b.adjust(1)
    await c.message.edit_text(text, reply_markup=b.as_markup())
    await c.answer()

@dp.callback_query(F.data == "back_home")
async def back_home(c: types.CallbackQuery):
    text = "Главное меню. Выберите раздел:"
    await c.message.edit_text(text, reply_markup=get_main_menu())
    await c.answer()

async def handle(request):
    return web.Response(text="OK")

async def web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

async def main():
    await web_server()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
