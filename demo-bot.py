import os
import logging
import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiohttp import web

# Токен твоего бота
TOKEN = "9074013397:AAGT4oqK1RwH2_xw9IP5I4sUMacLSCMqtO8"
ADMIN_USERNAME = "GoodBus1nesBot"  # Юзернейм для связи

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# === РАБОТА С БАЗОЙ ДАННЫХ (SQLite) ===
def init_db():
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()
    # Создаем таблицу клиентов, если она еще не создана
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

def save_client(telegram_id, username, full_name):
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT OR IGNORE INTO clients (telegram_id, username, full_name) VALUES (?, ?, ?)",
            (telegram_id, username, full_name)
        )
        conn.commit()
    except Exception as e:
        logging.error(f"Ошибка сохранения в БД: {e}")
    finally:
        conn.close()

# Инициализируем базу данных при запуске
init_db()

# === КЛАВИАТУРЫ ===
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

# === ХЕНДЛЕРЫ (ОБРАБОТЧИКИ) ===
@dp.message(Command("start"))
async def cmd_start(msg: types.Message):
    # Сохраняем пользователя в базу данных автоматически
    save_client(
        telegram_id=msg.from_user.id,
        username=msg.from_user
