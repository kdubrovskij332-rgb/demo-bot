import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiohttp import web

# Токен твоего бота
TOKEN = "9074013397:AAGT4oqK1RwH2_xw9IP5I4sUMacLSCMqtO8"
ADMIN_USERNAME = "GoodBus1nesBot"  # Юзернейм для связи и заказа услуг

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Главное меню (профессиональное оформление)
def get_main_menu():
    b = InlineKeyboardBuilder()
    b.button(text="🌐 Сетевые услуги и IT", callback_data="services")
    b.button(text="💼 Портфолио проектов", callback_data="portfolio")
    b.button(text="💳 Оплата и тарифы", callback_data="payment")
    b.button(text="📞 Связаться со специалистом", url=f"https://t.me/{ADMIN_USERNAME}")
    b.adjust(1)
    return b.as_markup()

# Кнопка «Назад»
def get_back_menu():
    b = InlineKeyboardBuilder()
    b.button(text="⬅️ Вернуться в главное меню", callback_data="back_home")
    b.adjust(1)
    return b.as_markup()

@dp.message(Command("start"))
async def cmd_start(msg: types.Message):
    welcome_text = (
        "👋 **Добро пожаловать!**\n\n"
        "Я — ваш персональный IT-помощник по профессиональному администрированию, "
        "построению и настройке сетевой инфраструктуры любой сложности.\n\n"
        "🛠 **Что мы делаем:**\n"
        "• Проектирование и монтаж локальных сетей (LAN/WAN)\n"
        "• Настройка маршрутизаторов, коммутаторов и корпоративного Wi-Fi\n"
        "• Администрирование систем и обеспечение информационной безопасности\n\n"
        "👇 *Выберите интересующий раздел в меню ниже:*"
    )
    await msg.answer(welcome_text, reply_markup=get_main_menu(), parse_mode="Markdown")

@dp.callback_query(F.data == "services")
async def show_services(c: types.CallbackQuery):
    text = (
        "🌐 **Наши ключевые сетевые решения:**\n\n"
        "1️⃣ **Локальные и глобальные сети (LAN/WAN)**\n"
        "   • Проектирование, монтаж кабельных трасс и кроссировка (RJ45)\n"
        "   • Объединение офисов в единую защищенную сеть (VPN)\n\n"
        "2️⃣ **Настройка сетевого оборудования**\n"
        "   • Конфигурация маршрутизаторов и коммутаторов (MikroTik, Cisco, TP-Link)\n"
        "   • Настройка VLAN, TRUNK-портов и маршрутизации трафика\n\n"
        "3️⃣ **Системное администрирование**\n"
        "   • Развертывание и поддержка Active Directory, виртуальных машин (VirtualBox)\n"
        "   • Организация резервного копирования и мониторинга 24/7"
    )
    await c.message.edit_text(text, reply_markup=get_back_menu(), parse_mode="Markdown")
    await c.answer()

@dp.callback_query(F.data == "portfolio")
async def show_portfolio(c: types.CallbackQuery):
    text = (
        "💼 **Примеры успешных проектов:**\n\n"
        "🏢 **Офис под ключ (150 рабочих мест)**\n"
        "   • Полноценный монтаж структурированной кабельной системы (СКС)\n"
        "   • Настройка бесшовного корпоративного Wi-Fi и сегментация сети через VLAN\n\n"
        "🏭 **Складской комплекс**\n"
        "   • Организация стабильного сетевого покрытия по всей территории\n"
        "   • Интеграция систем видеонаблюдения и контроля доступа\n\n"
        "🏠 **Частные корпоративные сети**\n"
        "   • Защищенные шлюзы, родительский контроль и удаленный доступ"
    )
    await c.message.edit_text(text, reply_markup=get_back_menu(), parse_mode="Markdown")
    await c.answer()

@dp.callback_query(F.data == "payment")
async def show_payment(c: types.CallbackQuery):
    text = (
        "💳 **Способы оплаты и порядок работы:**\n\n"
        "Мы работаем как с физическими, так и с юридическими лицами. Доступные варианты расчета:\n\n"
        "• 🟢 **Банковская карта** (Перевод на карту / реквизиты)\n"
        "• 📄 **Безналичный расчет** (Оплата по выставленному счету для компаний)\n"
        "•  USDT / Криптовалюта (по предварительному согласованию)\n\n"
        "📌 *Для заказа выезда специалиста или консультации нажмите кнопку ниже.*"
    )
    
    # Кнопки для раздела оплаты: назад + связь
    b = InlineKeyboardBuilder()
    b.button(text="📞 Связаться для уточнения реквизитов", url=f"https://t.me/{ADMIN_USERNAME}")
    b.button(text="⬅️ Вернуться в главное меню", callback_data="back_home")
    b.adjust(1)
    
    await c.message.edit_text(text, reply_markup=b.as_markup(), parse_mode="Markdown")
    await c.answer()

@dp.callback_query(F.data == "back_home")
async def back_home(c: types.CallbackQuery):
    text = "🏠 **Главное меню.** Выберите интересующий раздел:"
    await c.message.edit_text(text, reply_markup=get_main_menu(), parse_mode="Markdown")
    await c.answer()

# Веб-сервер для стабильной работы на Render (исключает ошибку портов)
async def handle(request):
    return web.Response(text="Network Service Bot is running!")

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
