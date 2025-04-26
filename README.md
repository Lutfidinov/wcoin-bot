# wcoin-bot
Bu bot telegram gruppa uchun
# WCOIN-BOT

## Loyihaning tavsifi
WCOIN-BOT — bu Telegram bot bo‘lib, foydalanuvchilar:
- Referal orqali tanga olishadi,
- Tanga balanslarini ko‘rishadi,
- Bir-birlariga tanga yuborishadi,
- Admin orqali to‘lov qilishadi.

## Texnologiyalar
- Python 3.9+
- Aiogram
- SQLite
- Dotenv

## O'rnatish

```bash
git clone https://github.com/sening-username/wcoin-bot.git
cd wcoin-bot
pip install -r requirements.txt
Sozlash
config.py faylini o'zgartiring:

python
Копировать
Редактировать
API_TOKEN = 'YOUR_BOT_TOKEN'
ADMIN_ID = 123456789
Ishga tushirish
bash
Копировать
Редактировать
python bot.py
Loyihaning tuzilmasi
bot.py — Asosiy bot logikasi

config.py — Konfiguratsiya parametrlari

database/ — SQLite bilan ishlash

handlers/ — Buyruq va voqealarni boshqarish

utils/ — Yordamchi funksiyalar

Muallif
Avazxon Lutfidinov (aka @AvazxonL)

yaml
Копировать
Редактировать

---

# 🛠 requirements.txt

```txt
aiogram==2.25.1
python-dotenv==1.0.1
(sqlite3 - Python ichiga o‘rnatilgan, alohida qo‘shilmaydi.)
