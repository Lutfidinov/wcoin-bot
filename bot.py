import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from config import TOKEN

# BAZA bilan ulanamiz (agar bo'lmasa yaratamiz)
db = sqlite3.connect('users.db')
sql = db.cursor()

# Users jadvalini yaratamiz (agar mavjud bo'lmasa)
sql.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        balance INTEGER DEFAULT 0,
        referals INTEGER DEFAULT 0,
        inviter INTEGER
    )
''')
db.commit()

# BOT va DISPATCHER yaratamiz
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# START komandasi
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    user_id = message.from_user.id

    # Foydalanuvchi bazada bormi tekshiramiz
    sql.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
    user = sql.fetchone()

    if not user:
        # Agar foydalanuvchi yangi bo'lsa
        inviter_id = None
        if message.get_args():
            try:
                inviter_id = int(message.get_args())
            except ValueError:
                pass

        sql.execute('INSERT INTO users (user_id, inviter) VALUES (?, ?)', (user_id, inviter_id))
        db.commit()

        if inviter_id:
            sql.execute('UPDATE users SET referals = referals + 1 WHERE user_id = ?', (inviter_id,))
            sql.execute('UPDATE users SET balance = balance + 10 WHERE user_id = ?', (inviter_id,))
            db.commit()

    # Referal link
    referal_link = f"https://t.me/{(await bot.get_me()).username}?start={user_id}"

    await message.answer(
        f"Salom, {message.from_user.first_name}!\n"
        f"👥 Referal link: {referal_link}\n\n"
        f"Do'stlaringizni taklif qiling va har bir do'stingiz uchun 10 tanga oling!"
    )

# BALANCE komandasi
@dp.message_handler(commands=['balance'])
async def balance_command(message: types.Message):
    user_id = message.from_user.id
    sql.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,))
    balance = sql.fetchone()

    if balance:
        await message.answer(f"💰 Sizning balansingiz: {balance[0]} tanga.")
    else:
        await message.answer("Siz ro'yxatdan o'tmagansiz. /start ni bosing.")

# PAY komandasi (Admin uchun)
@dp.message_handler(commands=['pay'])
async def pay_command(message: types.Message):
    ADMIN_ID = 1851325805  # << BU YERGA O'ZING ADMIN ID INGNI QOY!
    if message.from_user.id != ADMIN_ID:
        await message.answer("Sizda bu buyruqni ishlatish huquqi yo'q.")
        return

    try:
        command, user_id, amount = message.text.split()
        user_id = int(user_id)
        amount = int(amount)
    except:
        await message.answer("Foydalanish: /pay user_id miqdor")
        return

    sql.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (amount, user_id))
    db.commit()
    await message.answer(f"{user_id} foydalanuvchiga {amount} tanga yuborildi!")

# TRANSFER komandasi (foydalanuvchi foydalanuvchiga pul yuboradi)
@dp.message_handler(commands=['transfer'])
async def transfer_command(message: types.Message):
    try:
        command, receiver_id, amount = message.text.split()
        receiver_id = int(receiver_id)
        amount = int(amount)
    except:
        await message.answer("Foydalanish: /transfer user_id miqdor")
        return

    sender_id = message.from_user.id

    # Jo'natuvchi balansini tekshiramiz
    sql.execute('SELECT balance FROM users WHERE user_id = ?', (sender_id,))
    sender_balance = sql.fetchone()

    if not sender_balance or sender_balance[0] < amount:
        await message.answer("Sizda yetarlicha mablag' yo'q.")
        return

    # Oluvchi mavjudligini tekshiramiz
    sql.execute('SELECT balance FROM users WHERE user_id = ?', (receiver_id,))
    receiver_balance = sql.fetchone()

    if not receiver_balance:
        await message.answer("Qabul qiluvchi topilmadi.")
        return

    # Pulni o'tkazamiz
    sql.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (amount, sender_id))
    sql.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (amount, receiver_id))
    db.commit()

    await message.answer(f"Siz {receiver_id} foydalanuvchiga {amount} tanga yubordingiz.")

# BOTNI ISHGA TUSHURAMIZ
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
