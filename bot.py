import telebot
import random
import sqlite3
import time
from telebot import types

BOT_TOKEN = "8912679005:AAHNqMC7pJxRrQu5mEoIGqLwgKDFnESatjs"
ADMIN_ID = 8481806014
GIFT_ID = "heart"
RAPIRA_ID = "153935"
ADMIN_USERNAME = "ertywrate"

bot = telebot.TeleBot(BOT_TOKEN)

conn = sqlite3.connect("bot.db", check_same_thread=False)
UPGRADE_REQUESTS = {}

def init_db():
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username TEXT, balance INTEGER DEFAULT 100, referrer_id INTEGER)""")
    c.execute("""CREATE TABLE IF NOT EXISTS inventory (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, item TEXT, rarity TEXT, price INTEGER)""")
    c.execute("""CREATE TABLE IF NOT EXISTS withdraws (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, item TEXT, rarity TEXT, status TEXT DEFAULT 'pending')""")
    try:
        c.execute("""ALTER TABLE users ADD COLUMN spent INTEGER DEFAULT 0""")
    except:
        pass
    try:
        c.execute("""ALTER TABLE users ADD COLUMN gold INTEGER DEFAULT 0""")
    except:
        pass
    conn.commit()

init_db()

SHOP = {
    "1": {"name": "AK74 Выживший", "price": 5},
    "2": {"name": "M416 Маньяк", "price": 5},
    "3": {"name": "UMP Агрессор", "price": 20},
    "4": {"name": "M416 Реактор", "price": 100},
    "5": {"name": "AK74 Вандал", "price": 2000},
    "6": {"name": "AK74 Хакер", "price": 5000},
    "7": {"name": "Deagle Ледяной взгляд", "price": 8000},
    "8": {"name": "Керамбит Сафари", "price": 15000},
    "9": {"name": "Бабочка Изумруд", "price": 25000},
    "10": {"name": "Складной нож Индиго", "price": 40000},
}

SKINS = {
    "trash": [
        ("AK74 Выживший", 1), ("M416 Маньяк", 1), ("G17 Эпоха", 1),
        ("Deagle Антиквариат", 1), ("AK74 Вязаный", 1), ("MP7 Мозаика", 1),
        ("G17 Антиквариат", 1), ("ShortGun Антиквариат", 1), ("AWM Капрал", 1),
        ("Deagle Лес", 1), ("BM1014 Стингер", 1), ("Агент Браконьер", 1),
        ("SIG556 Титан", 1), ("ShortGun Игра окончена", 1), ("FAMAS Стингер", 1),
        ("Агент Пустынный призрак", 1), ("M416 СССР", 1), ("P90 Вендетта", 1),
        ("FAMAS Тигр", 1), ("SIG556 Механизатор", 1), ("SIG556 Одно нажатие", 1),
        ("FS Биологическая угроза", 2), ("G17 Карбон", 4), ("UMP Лабиринт", 2),
        ("Benelli Закат", 2), ("Агент Чанк", 2), ("BM1014 Демон", 2),
        ("FS Полный заряд", 4), ("FS Гоярд", 4), ("ShortGun Гоярд", 2),
        ("P90 Хром", 5), ("Граффити Вопросы?", 5), ("Граффити Без огнестрела", 5),
        ("Граффити GG EZZZY", 5), ("Граффити ЛOX", 5),
    ],
    "almost": [
        ("UMP Агрессор", 7), ("MK20 Охотник", 3), ("FAMAS Ангел-Хранитель", 6),
        ("Deagle Красная молния", 9), ("Граффити Хэдшот", 10),
        ("Граффити Остынь", 10), ("AUG Байкер", 3),
    ],
    "low": [
        ("Граффити W", 20), ("Граффити Соло", 20), ("Граффити RAPIRA", 23),
        ("Граффити Туз бубновый", 20), ("Агент Сейм-младший", 15),
        ("M416 Реактор", 34), ("PM Пустынный", 38), ("USP-S Развертка", 31),
        ("M416 Вертекс", 21), ("MP7 Число удачи", 14), ("P320 Оверлок", 16),
        ("AWM Киберспорт", 50), ("PM Кровавый закат", 50),
        ("Берет Багровое небо", 20), ("P90 Критичость", 27), ("FS Шаман", 20),
        ("Агент Ветеран Чанк", 20), ("MP7 Паутина", 29), ("MAC11 Котака", 20),
        ("MAC11 ул. Риверсайд", 34), ("G17 Проект Икс", 40),
        ("AUG Критичность", 41), ("P320 Тотем", 19), ("Deagle Ярость", 50),
        ("MP7 Горящая паутина", 20), ("Агент Красный орел", 45),
        ("Граффити Керамбит", 60), ("Граффити Король", 90),
    ],
    "mid": [
        ("AK74 Пламя", 95), ("M416 Градиент", 114), ("AWM Дикий лес", 140),
        ("FAMAS Пожиратель", 180), ("Граффити Первый уровень", 100),
        ("ACE52 Деймос", 60),
    ],
    "high": [
        ("AK74 Хакер", 349), ("Deagle Градиент", 298), ("USP-S Градиент", 300),
        ("Deagle Огненный дракон", 410), ("AWM Древнее зло", 640),
        ("MAC11 Вебстер", 450), ("M416 Ривер Войд", 500), ("AK74 Вандал", 670),
        ("Агент Рядовой Чанк", 390), ("P320 Сакура", 500), ("PM Призрак", 345),
        ("G17 Последний закат", 230),
    ],
    "top": [
        ("Deagle Ледяной взгляд", 1500),
    ],
    "secret_cheap": [
        ("Винтажные перчатки Майами", 2000),
        ("Бабочка Ледяной взгляд", 1950),
        ("Керамбит Огненный градиент", 1400),
        ("M9 Кибер-кость", 2000),
        ("M9 Рубин", 2200),
        ("Винтажные перчатки Красная заря", 1900),
        ("Керамбит Хищник", 1400),
        ("M9 Ледяной взгляд", 1875),
        ("Тактические перчатки Арктический хищник", 1175),
        ("Керамбит Сафари", 1450),
        ("Тактические перчатки Пчела", 999),
        ("Спортивные перчатки Пламя", 1195),
    ],
    "secret_top": [
        ("Бабочка Изумруд", 3600),
        ("Бабочка Темная материя", 3495),
        ("Винтажные перчатки Эльф", 3333),
        ("Байкерские перчатки Разгон", 3000),
        ("Складной нож Индиго", 3895),
    ],
}
def get_user(user_id):
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    return c.fetchone()

def create_user(user_id, username, referrer_id=None):
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id, username, referrer_id) VALUES (?, ?, ?)",
              (user_id, username, referrer_id))
    conn.commit()

def update_balance(user_id, amount):
    c = conn.cursor()
    c.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, user_id))
    conn.commit()

def main_menu():
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("👤 Профиль", callback_data="profile"),
        types.InlineKeyboardButton("🎒 Инвентарь", callback_data="inventory"),
        types.InlineKeyboardButton("🛒 Купить скины", callback_data="shop"),
        types.InlineKeyboardButton("💳 Пополнить", callback_data="topup"),
        types.InlineKeyboardButton("🔄 Апгрейд", callback_data="upgrade"),
        types.InlineKeyboardButton("💰 Голда", callback_data="buy_gold"),
        types.InlineKeyboardButton("🎲 Кубик", callback_data="dice"),
        types.InlineKeyboardButton("🎯 Дартс", callback_data="darts"),
        types.InlineKeyboardButton("🏆 Рейтинг", callback_data="rating"),
        types.InlineKeyboardButton("💬 Поддержка", callback_data="support"),
    )
    return kb

def send_menu(chat_id, message_id=None):
    user = get_user(chat_id)
    gold = user[5] if len(user) > 5 else 0
    admin_mark = "👑 Ты админ!\n\n" if chat_id == ADMIN_ID else ""
    text = (
        f"🐉 Добро пожаловать, путник!\n\n"
        f"{admin_mark}"
        f"Это бот по Rapira.\n"
        f"Апгрейди скины, покупай голду, поднимайся в рейтинге!\n\n"
        f"💳 Баланс: {user[2]} монет\n"
        f"💰 Голда: {gold}"
    )
    if message_id:
        try:
            bot.delete_message(chat_id, message_id)
        except:
            pass
    try:
        with open("logo.png", "rb") as photo:
            bot.send_photo(chat_id, photo, caption=text, reply_markup=main_menu())
    except:
        bot.send_message(chat_id, text, reply_markup=main_menu())

@bot.message_handler(commands=['addbalance'])
def add_balance_cmd(message):
    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, "❌ Нет доступа.")
        return
    try:
        parts = message.text.split()
        user_id = int(parts[1])
        amount = int(parts[2])
        update_balance(user_id, amount)
        bot.send_message(message.chat.id, f"✅ Пользователю {user_id} начислено {amount} монет.")
    except:
        bot.send_message(message.chat.id, "❌ Формат: /addbalance ID СУММА")

@bot.message_handler(commands=['addgold'])
def add_gold_cmd(message):
    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, "❌ Нет доступа.")
        return
    try:
        parts = message.text.split()
        user_id = int(parts[1])
        amount = int(parts[2])
        c = conn.cursor()
        c.execute("UPDATE users SET gold = gold + ? WHERE user_id = ?", (amount, user_id))
        conn.commit()
        bot.send_message(message.chat.id, f"✅ Пользователю {user_id} начислено {amount} голды.")
        bot.send_message(user_id, f"✅ Тебе зачислено {amount} голды!")
    except:
        bot.send_message(message.chat.id, "❌ Формат: /addgold ID СУММА")

@bot.message_handler(commands=['confirm_skin'])
def confirm_skin(message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        parts = message.text.split()
        user_id = int(parts[1])
        price = int(parts[2])
        skin_name = " ".join(parts[3:])
        c = conn.cursor()
        c.execute("INSERT INTO inventory (user_id, item, rarity, price) VALUES (?, ?, 'upgrade', ?)",
                  (user_id, skin_name, price))
        conn.commit()
        bot.send_message(user_id, f"✅ Твой скин {skin_name} ({price} голды) зачислен в инвентарь!")
        bot.send_message(ADMIN_ID, f"✅ Скин {skin_name} ({price}) зачислен игроку {user_id}")
    except:
        bot.send_message(ADMIN_ID, "❌ Формат: /confirm_skin ID ЦЕНА Название")

@bot.message_handler(commands=['start'])
def start(message):
    args = message.text.split()
    referrer_id = int(args[1]) if len(args) > 1 and args[1].isdigit() else None
    user = get_user(message.from_user.id)
    if not user:
        create_user(message.from_user.id, message.from_user.username, referrer_id)
        if referrer_id:
            update_balance(referrer_id, 10)
    send_menu(message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == "profile")
def profile(call):
    user = get_user(call.from_user.id)
    gold = user[5] if len(user) > 5 else 0
    admin_mark = "👑 Админ\n" if call.from_user.id == ADMIN_ID else ""
    text = (
        f"👤 Профиль\n\n{admin_mark}"
        f"ID: {user[0]}\n"
        f"💳 Баланс: {user[2]} монет\n"
        f"💰 Голда: {gold}\n"
        f"⭐ Потрачено: {user[4]} звёзд\n"
        f"Реф-ссылка: https://t.me/{(bot.get_me()).username}?start={user[0]}"
    )
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("⬅️ Назад", callback_data="back"))
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    bot.send_message(call.message.chat.id, text, reply_markup=kb)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "inventory")
def inventory(call):
    c = conn.cursor()
    c.execute("SELECT id, item, rarity, price FROM inventory WHERE user_id = ?", (call.from_user.id,))
    items = c.fetchall()
    if not items:
        text = "🎒 Инвентарь пуст."
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("⬅️ Назад", callback_data="back"))
    else:
        text = "🎒 Твой инвентарь:\n\n"
        kb = types.InlineKeyboardMarkup(row_width=1)
        for item_id, item, rarity, price in items:
            text += f"• {item} ({rarity}) — {price} голды\n"
            kb.add(
                types.InlineKeyboardButton(f"💰 Продать {item} ({price})", callback_data=f"sell_{item_id}"),
                types.InlineKeyboardButton(f"📤 Вывести {item}", callback_data=f"withdraw_{item_id}")
            )
        kb.add(types.InlineKeyboardButton("⬅️ Назад", callback_data="back"))
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    try:
        with open("inventory.png", "rb") as photo:
            bot.send_photo(call.message.chat.id, photo, caption=text, reply_markup=kb)
    except:
        bot.send_message(call.message.chat.id, text, reply_markup=kb)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("sell_"))
def sell_item(call):
    item_id = int(call.data.split("_")[1])
    c = conn.cursor()
    c.execute("SELECT item, price FROM inventory WHERE id = ? AND user_id = ?",
              (item_id, call.from_user.id))
    item = c.fetchone()
    if not item:
        bot.answer_callback_query(call.id, "Скин не найден!", show_alert=True)
        return
    price = item[1]
    c.execute("DELETE FROM inventory WHERE id = ?", (item_id,))
    conn.commit()
    update_balance(call.from_user.id, price)
    bot.answer_callback_query(call.id, f"✅ Продано за {price} монет!")
    inventory(call)

@bot.callback_query_handler(func=lambda call: call.data.startswith("withdraw_"))
def withdraw(call):
    item_id = int(call.data.split("_")[1])
    c = conn.cursor()
    c.execute("SELECT item, rarity FROM inventory WHERE id = ? AND user_id = ?",
              (item_id, call.from_user.id))
    item = c.fetchone()
    if not item:
        bot.answer_callback_query(call.id, "Скин не найден!", show_alert=True)
        return
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("✅ Да", callback_data=f"confirm_withdraw_{item_id}"),
        types.InlineKeyboardButton("❌ Отмена", callback_data="inventory"),
    )
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    bot.send_message(
        call.message.chat.id,
        f"❓ Вы точно хотите вывести этот скин?\n\n🎁 Скин: {item[0]}\n⭐ Редкость: {item[1]}",
        reply_markup=kb
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("confirm_withdraw_"))
def confirm_withdraw(call):
    item_id = int(call.data.split("_")[2])
    c = conn.cursor()
    c.execute("SELECT item, rarity FROM inventory WHERE id = ? AND user_id = ?",
              (item_id, call.from_user.id))
    item = c.fetchone()
    if not item:
        bot.answer_callback_query(call.id, "Скин не найден!", show_alert=True)
        return
    c.execute("INSERT INTO withdraws (user_id, item, rarity) VALUES (?, ?, ?)",
              (call.from_user.id, item[0], item[1]))
    c.execute("DELETE FROM inventory WHERE id = ?", (item_id,))
    conn.commit()
    bot.send_message(ADMIN_ID,
        f"🔔 Заявка на вывод\nИгрок: {call.from_user.id}\nСкин: {item[0]} ({item[1]})")
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(types.InlineKeyboardButton("💬 Поддержка", callback_data="support"))
    kb.add(types.InlineKeyboardButton("✅ Подтвердить получение", callback_data=f"received_{item_id}"))
    text = (
        f"📤 Заявка на вывод создана!\n\n"
        f"🎁 Скин: {item[0]}\n"
        f"⭐ Редкость: {item[1]}\n\n"
        f"📌 Что делать:\n"
        f"1. Добавь в друзья в Rapira: {RAPIRA_ID}\n"
        f"2. В течение 15 минут будь онлайн в игре.\n"
        f"3. После получения скина — нажми «✅ Подтвердить получение».\n\n"
        f"🕐 Вывод работает: с 18:00 до 22:00 (МСК).\n"
        f"⏰ Если ты в другое время — заявка сохранится, выдам вечером.\n\n"
        f"⚠️ Не пиши «скам» — я реальный админ, всё выдам."
    )
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    try:
        with open("withdraw.png", "rb") as photo:
            bot.send_photo(call.message.chat.id, photo, caption=text, reply_markup=kb)
    except:
        bot.send_message(call.message.chat.id, text, reply_markup=kb)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("received_"))
def received(call):
    c = conn.cursor()
    c.execute("UPDATE withdraws SET status = 'done' WHERE user_id = ? AND status = 'pending'",
              (call.from_user.id,))
    conn.commit()
    bot.answer_callback_query(call.id, "✅ Спасибо! Заявка закрыта.")
    send_menu(call.message.chat.id, call.message.message_id)

@bot.callback_query_handler(func=lambda call: call.data == "shop")
def shop(call):
    user = get_user(call.from_user.id)
    kb = types.InlineKeyboardMarkup(row_width=1)
    for key, item in SHOP.items():
        kb.add(types.InlineKeyboardButton(f"{item['name']} — {item['price']} монет", callback_data=f"shop_buy_{key}"))
    kb.add(types.InlineKeyboardButton("⬅️ Назад", callback_data="back"))
    text = f"🛒 Магазин скинов\n\n💳 Твой баланс: {user[2]} монет\n\nВыбери скин:"
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    try:
        with open("shop.png", "rb") as photo:
            bot.send_photo(call.message.chat.id, photo, caption=text, reply_markup=kb)
    except:
        bot.send_message(call.message.chat.id, text, reply_markup=kb)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("shop_buy_"))
def shop_buy(call):
    key = call.data.split("_")[2]
    item = SHOP.get(key)
    if not item:
        bot.answer_callback_query(call.id, "Скин не найден!", show_alert=True)
        return
    user = get_user(call.from_user.id)
    if user[2] < item["price"]:
        bot.answer_callback_query(call.id, "Недостаточно монет!", show_alert=True)
        return
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("✅ Купить", callback_data=f"shop_ok_{key}"),
        types.InlineKeyboardButton("❌ Отмена", callback_data="shop"),
    )
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    bot.send_message(
        call.message.chat.id,
        f"❓ Купить {item['name']} за {item['price']} монет?\n\n💳 Баланс: {user[2]} монет",
        reply_markup=kb
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("shop_ok_"))
def shop_ok(call):
    key = call.data.split("_")[2]
    item = SHOP.get(key)
    if not item:
        bot.answer_callback_query(call.id, "Скин не найден!", show_alert=True)
        return
    user = get_user(call.from_user.id)
    if user[2] < item["price"]:
        bot.answer_callback_query(call.id, "Недостаточно монет!", show_alert=True)
        return
    c = conn.cursor()
    c.execute("UPDATE users SET balance = balance - ? WHERE user_id = ?", (item["price"], call.from_user.id))
    c.execute("INSERT INTO inventory (user_id, item, rarity, price) VALUES (?, ?, 'shop', ?)",
              (call.from_user.id, item["name"], item["price"]))
    conn.commit()
    bot.answer_callback_query(call.id, f"✅ Куплено: {item['name']}!")
    shop(call)

@bot.callback_query_handler(func=lambda call: call.data == "topup")
def topup(call):
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton("50 ⭐ = 100 монет", callback_data="pay_50"),
        types.InlineKeyboardButton("100 ⭐ = 220 монет (бонус +20)", callback_data="pay_100"),
        types.InlineKeyboardButton("250 ⭐ = 600 монет (бонус +100)", callback_data="pay_250"),
        types.InlineKeyboardButton("500 ⭐ = 1300 монет (бонус +300)", callback_data="pay_500"),
    )
    kb.add(types.InlineKeyboardButton("⬅️ Назад", callback_data="back"))
    text = "💳 Выбери сумму пополнения:\n\n1 звезда = 2 монеты\n🔥 Бонусы за крупные пополнения!"
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    try:
        with open("topup.png", "rb") as photo:
            bot.send_photo(call.message.chat.id, photo, caption=text, reply_markup=kb)
    except:
        bot.send_message(call.message.chat.id, text, reply_markup=kb)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("pay_"))
def pay(call):
    amount = int(call.data.split("_")[1])
    prices = [types.LabeledPrice(label=f"{amount} звёзд", amount=amount)]
    bot.send_invoice(
        call.message.chat.id,
        title=f"Пополнение",
        description=f"Баланс + монеты",
        invoice_payload=f"topup_{amount}",
        provider_token="",
        currency="XTR",
        prices=prices
    )
    bot.answer_callback_query(call.id)
@bot.callback_query_handler(func=lambda call: call.data == "buy_gold")
def buy_gold(call):
    user = get_user(call.from_user.id)
    gold = user[5] if len(user) > 5 else 0
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton("100 монет = 50 голды", callback_data="gold_100"),
        types.InlineKeyboardButton("500 монет = 300 голды", callback_data="gold_500"),
        types.InlineKeyboardButton("1000 монет = 700 голды", callback_data="gold_1000"),
        types.InlineKeyboardButton("2000 монет = 1600 голды", callback_data="gold_2000"),
    )
    kb.add(types.InlineKeyboardButton("🎰 Апгрейд голды", callback_data="gold_upgrade"))
    kb.add(types.InlineKeyboardButton(f"💬 Закинуть голду (@{ADMIN_USERNAME})", url=f"https://t.me/{ADMIN_USERNAME}"))
    kb.add(types.InlineKeyboardButton("⬅️ Назад", callback_data="back"))
    text = f"💰 Купить голду\n\nТвой баланс: {user[2]} монет\nТвоя голда: {gold}\n\n1 голда = ~1.5 монеты"
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    try:
        with open("gold.png", "rb") as photo:
            bot.send_photo(call.message.chat.id, photo, caption=text, reply_markup=kb)
    except:
        bot.send_message(call.message.chat.id, text, reply_markup=kb)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("gold_") and call.data != "gold_upgrade")
def gold_buy(call):
    amount = int(call.data.split("_")[1])
    gold = {100: 50, 500: 300, 1000: 700, 2000: 1600}[amount]
    user = get_user(call.from_user.id)
    if user[2] < amount:
        bot.answer_callback_query(call.id, "Недостаточно монет!", show_alert=True)
        return
    c = conn.cursor()
    c.execute("UPDATE users SET balance = balance - ?, gold = gold + ? WHERE user_id = ?",
              (amount, gold, call.from_user.id))
    conn.commit()
    bot.answer_callback_query(call.id, f"✅ Куплено {gold} голды!")
    buy_gold(call)

@bot.callback_query_handler(func=lambda call: call.data == "gold_upgrade")
def gold_upgrade(call):
    user = get_user(call.from_user.id)
    gold = user[5] if len(user) > 5 else 0
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton("🟢 Шанс 80% — ×1.2", callback_data="gmode_80"),
        types.InlineKeyboardButton("🟡 Шанс 65% — ×1.5", callback_data="gmode_65"),
        types.InlineKeyboardButton("🟠 Шанс 50% — ×1.8", callback_data="gmode_50"),
        types.InlineKeyboardButton("🔴 Шанс 30% — ×3.0", callback_data="gmode_30"),
    )
    kb.add(types.InlineKeyboardButton("⬅️ Назад", callback_data="buy_gold"))
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    bot.send_message(call.message.chat.id, f"🎰 Апгрейд голды\n\nТвоя голда: {gold}\n\nВыбери шанс:", reply_markup=kb)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("gmode_"))
def gmode(call):
    mode = int(call.data.split("_")[1])
    user = get_user(call.from_user.id)
    gold = user[5] if len(user) > 5 else 0
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("Ставить 50", callback_data=f"gup_{mode}_50"),
        types.InlineKeyboardButton("Ставить 100", callback_data=f"gup_{mode}_100"),
        types.InlineKeyboardButton("Ставить 500", callback_data=f"gup_{mode}_500"),
        types.InlineKeyboardButton("Ставить 1000", callback_data=f"gup_{mode}_1000"),
    )
    kb.add(types.InlineKeyboardButton("⬅️ Назад", callback_data="gold_upgrade"))
    mult = {80: 1.2, 65: 1.5, 50: 1.8, 30: 3.0}[mode]
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    bot.send_message(
        call.message.chat.id,
        f"🎰 Апгрейд голды\n\nТвоя голда: {gold}\nШанс: {mode}%\nМножитель: ×{mult}\n\nВыбери ставку:",
        reply_markup=kb
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("gup_"))
def gold_upgrade_go(call):
    parts = call.data.split("_")
    mode = int(parts[1])
    amount = int(parts[2])
    user = get_user(call.from_user.id)
    gold = user[5] if len(user) > 5 else 0
    if gold < amount:
        bot.answer_callback_query(call.id, "Недостаточно голды!", show_alert=True)
        return
    mult = {80: 1.2, 65: 1.5, 50: 1.8, 30: 3.0}[mode]
    roll = random.uniform(0, 100)
    c = conn.cursor()
    if roll <= mode:
        win = int(amount * (mult - 1))
        c.execute("UPDATE users SET gold = gold + ? WHERE user_id = ?", (win, call.from_user.id))
        conn.commit()
        bot.answer_callback_query(call.id, f"🎉 УСПЕХ! +{win} голды!", show_alert=True)
    else:
        c.execute("UPDATE users SET gold = gold - ? WHERE user_id = ?", (amount, call.from_user.id))
        conn.commit()
        bot.answer_callback_query(call.id, f"😢 ПРОВАЛ! -{amount} голды.", show_alert=True)
    gmode(call)
@bot.callback_query_handler(func=lambda call: call.data == "upgrade")
def upgrade_start(call):
    c = conn.cursor()
    c.execute("SELECT id, item, price FROM inventory WHERE user_id = ?", (call.from_user.id,))
    items = c.fetchall()
    kb = types.InlineKeyboardMarkup(row_width=1)
    if items:
        for item_id, item, price in items:
            kb.add(types.InlineKeyboardButton(f"{item} ({price} голды)", callback_data=f"upg_pick_{item_id}"))
    else:
        kb.add(types.InlineKeyboardButton("🎒 Инвентарь пуст", callback_data="inventory"))
    kb.add(types.InlineKeyboardButton("📥 Закинуть свой скин", callback_data="upg_add"))
    kb.add(types.InlineKeyboardButton(f"💰 Закинуть голду (@{ADMIN_USERNAME})", url=f"https://t.me/{ADMIN_USERNAME}"))
    kb.add(types.InlineKeyboardButton("💬 Поддержка", callback_data="support"))
    kb.add(types.InlineKeyboardButton("⬅️ Назад", callback_data="back"))
    text = (
        "🔄 Апгрейд скинов\n\n"
        "📌 Что делать:\n"
        "1. Выбери свой скин из инвентаря ниже.\n"
        "2. Выбери шанс.\n"
        "3. Крути."
    )
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    try:
        with open("upgrade.png", "rb") as photo:
            bot.send_photo(call.message.chat.id, photo, caption=text, reply_markup=kb)
    except:
        bot.send_message(call.message.chat.id, text, reply_markup=kb)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "upg_add")
def upg_add(call):
    kb = types.InlineKeyboardMarkup(row_width=1)
    num = 0
    for cat in SKINS:
        for name, price in SKINS[cat]:
            kb.add(types.InlineKeyboardButton(f"{name} ({price})", callback_data=f"upg_sel_{num}"))
            num += 1
    kb.add(types.InlineKeyboardButton("⬅️ Назад", callback_data="upgrade"))
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    bot.send_message(call.message.chat.id, "📥 Выбери скин, который хочешь закинуть:", reply_markup=kb)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("upg_sel_"))
def upg_sel(call):
    num = int(call.data.split("_")[2])
    skin_name = None
    price = 0
    idx = 0
    for cat in SKINS:
        for name, p in SKINS[cat]:
            if idx == num:
                skin_name = name
                price = p
                break
            idx += 1
        if skin_name:
            break
    if not skin_name:
        bot.answer_callback_query(call.id, "Скин не найден!", show_alert=True)
        return
    user_id = call.from_user.id
    UPGRADE_REQUESTS[user_id] = {"in": skin_name, "price": price}
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("✅ Да", callback_data=f"upg_send_{user_id}"),
        types.InlineKeyboardButton("❌ Отмена", callback_data="upgrade"),
    )
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    bot.send_message(
        call.message.chat.id,
        f"❓ Ты хочешь закинуть: {skin_name} ({price} голды)?\n\n"
        f"🕐 Приём скинов: с 18:00 до 22:00 (МСК).\n"
        f"⏰ Если ты в другое время — заявка сохранится, приму вечером.\n\n"
        f"⚠️ Не пиши «скам» — я реальный админ, всё приму.",
        reply_markup=kb
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("upg_send_"))
def upg_send(call):
    user_id = int(call.data.split("_")[2])
    data = UPGRADE_REQUESTS.get(user_id, {"in": "?", "price": 0})
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    bot.send_message(
        call.message.chat.id,
        f"📥 Заявка создана!\n\n📌 Добавь в друзья в Rapira: {RAPIRA_ID}\n⏰ Будь онлайн 5 минут.\n\n"
        f"🕐 Приём скинов: с 18:00 до 22:00 (МСК).\nПосле передачи скина — админ подтвердит."
    )
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("✅ Подтвердить выдачу", callback_data=f"adm_ok_{user_id}"))
    bot.send_message(
        ADMIN_ID,
        f"📥 Заявка на апгрейд\nИгрок: {user_id}\n📥 Закидывает: {data['in']} ({data['price']})\n\n"
        f"Передай скин в игре и нажми «✅ Подтвердить выдачу».",
        reply_markup=kb
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("adm_ok_"))
def adm_ok(call):
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "❌ Нет доступа.", show_alert=True)
        return
    user_id = int(call.data.split("_")[2])
    data = UPGRADE_REQUESTS.get(user_id, {"in": "?", "price": 0})
    skin_name = data["in"]
    price = data["price"]
    c = conn.cursor()
    c.execute("INSERT INTO inventory (user_id, item, rarity, price) VALUES (?, ?, 'upgrade', ?)",
              (user_id, skin_name, price))
    conn.commit()
    bot.send_message(user_id, f"✅ Твой скин {skin_name} ({price} голды) зачислен в инвентарь!")
    bot.send_message(ADMIN_ID, f"✅ Скин {skin_name} ({price}) зачислен игроку {user_id}")
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    bot.send_message(call.message.chat.id, f"✅ Заявка подтверждена!\nИгрок: {user_id}\nСкин: {skin_name}")
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("upg_pick_"))
def upgrade_pick(call):
    item_id = int(call.data.split("_")[2])
    c = conn.cursor()
    c.execute("SELECT item, price FROM inventory WHERE id = ? AND user_id = ?",
              (item_id, call.from_user.id))
    item = c.fetchone()
    if not item:
        bot.answer_callback_query(call.id, "Скин не найден!", show_alert=True)
        return
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton("🟢 Шанс 80% — ×1.2", callback_data=f"umode_{item_id}_80"),
        types.InlineKeyboardButton("🟡 Шанс 65% — ×1.5", callback_data=f"umode_{item_id}_65"),
        types.InlineKeyboardButton("🟠 Шанс 50% — ×1.8", callback_data=f"umode_{item_id}_50"),
        types.InlineKeyboardButton("🔴 Шанс 30% — ×3.0", callback_data=f"umode_{item_id}_30"),
    )
    kb.add(types.InlineKeyboardButton("⬅️ Назад", callback_data="upgrade"))
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    bot.send_message(
        call.message.chat.id,
        f"🔄 Твой скин: {item[0]} ({item[1]} голды)\n\nВыбери шанс:",
        reply_markup=kb
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("umode_"))
def upgrade_mode(call):
    parts = call.data.split("_")
    item_id = int(parts[1])
    mode = int(parts[2])
    c = conn.cursor()
    c.execute("SELECT item, price FROM inventory WHERE id = ? AND user_id = ?",
              (item_id, call.from_user.id))
    item = c.fetchone()
    if not item:
        bot.answer_callback_query(call.id, "Скин не найден!", show_alert=True)
        return
    my_price = item[1]
    mult = {80: 1.2, 65: 1.5, 50: 1.8, 30: 3.0}[mode]
    target_price = int(my_price * mult)
    # Ищем ближайший скин по цене (только дороже твоего)
    target_skin = f"Скин за {target_price}"
    best_diff = 999999
    for cat in SKINS:
        for name, p in SKINS[cat]:
            if p <= my_price:
                continue
            diff = abs(p - target_price)
            if diff < best_diff:
                best_diff = diff
                target_skin = name
                target_price = p
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("✅ Крутить", callback_data=f"upg_go_{item_id}_{target_price}_{mode}"),
        types.InlineKeyboardButton("❌ Отмена", callback_data="upgrade"),
    )
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    bot.send_message(
        call.message.chat.id,
        f"🔄 Апгрейд скина\n\n"
        f"🎁 Твой скин: {item[0]} ({my_price} голды)\n"
        f"🎲 Шанс: {mode}%\n"
        f"📤 Получишь: {target_skin} ({target_price} голды)\n\n"
        f"Крутить?",
        reply_markup=kb
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("upg_go_"))
def upgrade_go(call):
    parts = call.data.split("_")
    item_id = int(parts[2])
    target_price = int(parts[3])
    chance = int(parts[4])
    c = conn.cursor()
    c.execute("SELECT item, price FROM inventory WHERE id = ? AND user_id = ?",
              (item_id, call.from_user.id))
    item = c.fetchone()
    if not item:
        bot.answer_callback_query(call.id, "Скин не найден!", show_alert=True)
        return
    my_price = item[1]
    roll = random.uniform(0, 100)
    if roll <= chance:
        c.execute("DELETE FROM inventory WHERE id = ?", (item_id,))
        skin_name = f"Скин за {target_price}"
        best_diff = 999999
        for cat in SKINS:
            for name, p in SKINS[cat]:
                if p <= my_price:
                    continue
                diff = abs(p - target_price)
                if diff < best_diff:
                    best_diff = diff
                    skin_name = name
                    target_price = p
        c.execute("INSERT INTO inventory (user_id, item, rarity, price) VALUES (?, ?, 'upgrade', ?)",
                  (call.from_user.id, skin_name, target_price))
        conn.commit()
        text = (
            f"🎉 УСПЕХ!\n\n"
            f"Ты обменял {item[0]} ({my_price}) на {skin_name} ({target_price} голды)!\n"
            f"Шанс был: {chance}%"
        )
    else:
        c.execute("DELETE FROM inventory WHERE id = ?", (item_id,))
        conn.commit()
        text = (
            f"😢 ПРОВАЛ!\n\n"
            f"Ты потерял {item[0]} ({my_price} голды).\n"
            f"Шанс был: {chance}%, но не повезло."
        )
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    bot.send_message(call.message.chat.id, text, reply_markup=main_menu())
    bot.answer_callback_query(call.id)
# === КУБИК ===
@bot.callback_query_handler(func=lambda call: call.data == "dice")
def dice_menu(call):
    user = get_user(call.from_user.id)
    gold = user[5] if len(user) > 5 else 0
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("Ставка 50", callback_data="dice_stake_50"),
        types.InlineKeyboardButton("Ставка 100", callback_data="dice_stake_100"),
        types.InlineKeyboardButton("Ставка 500", callback_data="dice_stake_500"),
        types.InlineKeyboardButton("Ставка 1000", callback_data="dice_stake_1000"),
    )
    kb.add(types.InlineKeyboardButton("⬅️ Назад", callback_data="back"))
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    bot.send_message(
        call.message.chat.id,
        f"🎲 Кубик\n\nТвоя голда: {gold}\n\nВыбери ставку:",
        reply_markup=kb
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("dice_stake_"))
def dice_stake(call):
    stake = int(call.data.split("_")[2])
    user = get_user(call.from_user.id)
    gold = user[5] if len(user) > 5 else 0
    if gold < stake:
        bot.answer_callback_query(call.id, "Недостаточно голды!", show_alert=True)
        return
    kb = types.InlineKeyboardMarkup(row_width=3)
    for i in range(1, 7):
        kb.add(types.InlineKeyboardButton(f"🎲 {i}", callback_data=f"dice_bet_{stake}_{i}"))
    kb.add(types.InlineKeyboardButton("⬅️ Назад", callback_data="dice"))
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    bot.send_message(
        call.message.chat.id,
        f"🎲 Кубик\n\nСтавка: {stake} голды\nМножитель: ×5\n\nВыбери число (1–6):",
        reply_markup=kb
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("dice_bet_"))
def dice_bet(call):
    parts = call.data.split("_")
    stake = int(parts[2])
    number = int(parts[3])
    user = get_user(call.from_user.id)
    gold = user[5] if len(user) > 5 else 0
    if gold < stake:
        bot.answer_callback_query(call.id, "Недостаточно голды!", show_alert=True)
        return
    c = conn.cursor()
    c.execute("UPDATE users SET gold = gold - ? WHERE user_id = ?", (stake, call.from_user.id))
    conn.commit()
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    msg = bot.send_dice(call.message.chat.id, emoji="🎲")
    time.sleep(3)
    result = msg.dice.value
    if result == number:
        win = stake * 5
        c.execute("UPDATE users SET gold = gold + ? WHERE user_id = ?", (win, call.from_user.id))
        conn.commit()
        bot.send_message(call.message.chat.id, f"🎉 Угадал! Выпало {result}.\nВыигрыш: +{win} голды!", reply_markup=main_menu())
    else:
        bot.send_message(call.message.chat.id, f"😢 Не угадал. Выпало {result}, а ты выбрал {number}.\nПотерял {stake} голды.", reply_markup=main_menu())
    bot.answer_callback_query(call.id)

# === ДАРТС ===
@bot.callback_query_handler(func=lambda call: call.data == "darts")
def darts_menu(call):
    user = get_user(call.from_user.id)
    gold = user[5] if len(user) > 5 else 0
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("Ставка 50", callback_data="darts_stake_50"),
        types.InlineKeyboardButton("Ставка 100", callback_data="darts_stake_100"),
        types.InlineKeyboardButton("Ставка 500", callback_data="darts_stake_500"),
        types.InlineKeyboardButton("Ставка 1000", callback_data="darts_stake_1000"),
    )
    kb.add(types.InlineKeyboardButton("⬅️ Назад", callback_data="back"))
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    bot.send_message(
        call.message.chat.id,
        f"🎯 Дартс\n\nТвоя голда: {gold}\n\nВыбери ставку:",
        reply_markup=kb
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("darts_stake_"))
def darts_stake(call):
    stake = int(call.data.split("_")[2])
    user = get_user(call.from_user.id)
    gold = user[5] if len(user) > 5 else 0
    if gold < stake:
        bot.answer_callback_query(call.id, "Недостаточно голды!", show_alert=True)
        return
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton("⚪ Белое ×2", callback_data=f"darts_bet_{stake}_white"),
        types.InlineKeyboardButton("🔴 Красное ×2", callback_data=f"darts_bet_{stake}_red"),
        types.InlineKeyboardButton("🟢 Центр ×14", callback_data=f"darts_bet_{stake}_center"),
    )
    kb.add(types.InlineKeyboardButton("⬅️ Назад", callback_data="darts"))
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    bot.send_message(
        call.message.chat.id,
        f"🎯 Дартс\n\nСтавка: {stake} голды\n\nВыбери сектор:",
        reply_markup=kb
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("darts_bet_"))
def darts_bet(call):
    parts = call.data.split("_")
    stake = int(parts[2])
    choice = parts[3]
    user = get_user(call.from_user.id)
    gold = user[5] if len(user) > 5 else 0
    if gold < stake:
        bot.answer_callback_query(call.id, "Недостаточно голды!", show_alert=True)
        return
    c = conn.cursor()
    c.execute("UPDATE users SET gold = gold - ? WHERE user_id = ?", (stake, call.from_user.id))
    conn.commit()
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    msg = bot.send_dice(call.message.chat.id, emoji="🎯")
    time.sleep(3)
    result = msg.dice.value
    if result == 1:
        result_color = "center"
        result_text = "🟢 Центр (1)"
    elif result == 2:
        result_color = "red"
        result_text = "🔴 Красное (2)"
    elif result == 3:
        result_color = "white"
        result_text = "⚪ Белое (3)"
    elif result == 4:
        result_color = "red"
        result_text = "🔴 Красное (4)"
    elif result == 5:
        result_color = "white"
        result_text = "⚪ Белое (5)"
    else:
        result_color = "red"
        result_text = "🔴 Красное (6)"
    if choice == result_color:
        if result_color == "center":
            win = stake * 14
        else:
            win = stake * 2
        c.execute("UPDATE users SET gold = gold + ? WHERE user_id = ?", (win, call.from_user.id))
        conn.commit()
        bot.send_message(call.message.chat.id, f"🎉 Выпало: {result_text}\nВыигрыш: +{win} голды!", reply_markup=main_menu())
    else:
        bot.send_message(call.message.chat.id, f"😢 Выпало: {result_text}\nПотерял {stake} голды.", reply_markup=main_menu())
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "rating")
def rating(call):
    c = conn.cursor()
    c.execute("SELECT user_id, username, balance FROM users WHERE user_id != ? ORDER BY balance DESC LIMIT 10", (ADMIN_ID,))
    top = c.fetchall()
    text = "🏆 Топ-10 по балансу:\n\n"
    if not top or all(t[2] == 0 for t in top):
        text += "Пока никого нет."
    else:
        for i, (uid, uname, balance) in enumerate(top, 1):
            name = f"@{uname}" if uname else f"ID {uid}"
            text += f"{i}. {name} — {balance} монет\n"
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("⬅️ Назад", callback_data="back"))
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    bot.send_message(call.message.chat.id, text, reply_markup=kb)
    bot.answer_callback_query(call.id)

@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(query):
    bot.answer_pre_checkout_query(query.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    amount = int(message.successful_payment.invoice_payload.split("_")[1])
    bonuses = {50: 100, 100: 220, 250: 600, 500: 1300}
    coins = bonuses.get(amount, amount * 2)
    update_balance(message.from_user.id, coins)
    c = conn.cursor()
    c.execute("UPDATE users SET spent = spent + ? WHERE user_id = ?", (amount, message.from_user.id))
    conn.commit()
    bot.send_message(message.chat.id, f"✅ Баланс пополнен на {coins} монет!")

@bot.callback_query_handler(func=lambda call: call.data == "support")
def support(call):
    msg = bot.send_message(call.message.chat.id, "✍️ Напиши свой вопрос или проблему — я передам админу.")
    bot.register_next_step_handler(msg, send_support)

def send_support(message):
    bot.send_message(ADMIN_ID,
        f"💬 Поддержка\nИгрок: {message.from_user.id} (@{message.from_user.username})\nСообщение: {message.text}")
    bot.send_message(message.chat.id, "✅ Сообщение отправлено админу. Ожидай ответа.", reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: call.data == "back")
def back(call):
    send_menu(call.message.chat.id, call.message.message_id)
    bot.answer_callback_query(call.id)

print("Бот запущен...")
while True:
    try:
        bot.polling(none_stop=True, timeout=60, long_polling_timeout=60)
    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(5)
              
        
        
        