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
        username=msg.from_user.username or "No username",
        full_name=msg.from_user.full_name or "No name"
    )
    
    welcome_text = (
        "👋 **Добро пожаловать в профессиональный IT-сервис!**\n\n"
        "Мы специализируемся на проектировании, настройке и администрировании сетевой инфраструктуры любой сложности.\n\n"
        "🛠 **Наши ключевые направления:**\n"
        "• Локальные и глобальные сети (LAN/WAN, VPN)\n"
        "• Конфигурация оборудования (MikroTik, Cisco, TP-Link)\n"
        "• Системное администрирование и безопасность\n\n"
        "👇 *Выберите интересующий раздел в меню ниже:*"
    )
    await msg.answer(welcome_text, reply_markup=get_main_menu(), parse_mode="Markdown")

@dp.callback_query(F.data == "services")
async def show_services(c: types.CallbackQuery):
    text = (
        "🌐 **Наши ключевые сетевые решения:**\n\n"
        "1️⃣ **Локальные и глобальные сети (LAN/WAN)**\n"
        "   • Проектирование, монтаж кабельных трасс и кроссировка (RJ45)\n"
        "   • Объединение удаленных офисов в защищенную сеть (VPN)\n\n"
        "2️⃣ **Настройка сетевого оборудования**\n"
        "   • Конфигурация маршрутизаторов и коммутаторов (MikroTik, Cisco)\n"
        "   • Настройка VLAN, TRUNK-портов и маршрутизации трафика\n\n"
        "3️⃣ **Системное администрирование**\n"
        "   • Развертывание и поддержка Active Directory, виртуальных сред\n"
        "   • Организация резервного копирования и мониторинга 24/7"
    )
    await c.message.edit_text(text, reply_markup=get_back_menu(), parse_mode="Markdown")
    await c.answer()

@dp.callback_query(F.data == "portfolio")
async def show_portfolio(c: types.CallbackQuery):
    text = (
        "💼 **Примеры успешных проектов:**\n\n"
        "🏢 **Корпоративный офис (150+ рабочих мест)**\n"
        "   • Полноценный монтаж СКС и кроссировка коммутационных шкафов\n"
        "   • Настройка бесшовного корпоративного Wi-Fi и сегментация через VLAN\n\n"
        "🏭 **Складской логистический комплекс**\n"
        "   • Организация отказоустойчивой сети на базе оборудования MikroTik\n"
        "   • Интеграция систем видеонаблюдения и контроля доступа\n\n"
        "🏠 **Частные защищенные сети**\n"
        "   • Высокоскоростные роутеры, безопасность и удаленный доступ"
    )
    await c.message.edit_text(text, reply_markup=get_back_menu(), parse_mode="Markdown")
    await c.answer()

@dp.callback_query(F.data == "payment")
async def show_payment(c: types.CallbackQuery):
    text = (
        "💳 **Способы оплаты и порядок работы:**\n\n"
        "Мы работаем официально с физическими и юридическими лицами:\n\n"
        "• 🟢 **Банковская карта** (Перевод по реквизитам)\n"
        "• 📄 **Безналичный расчет** (Оплата по счету для компаний)\n"
        "• 💎 **Криптовалюта** (USDT — по согласова
