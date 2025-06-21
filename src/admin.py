


import json
from telegram import Update
from telegram.ext import ContextTypes
from functools import wraps


ADMIN_IDS= {}
admin_add_state = {}

def cargar_admins():
    global ADMIN_IDS
    try:
        with open("../BD/admins.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            ADMIN_IDS = data.get("admins", [])
    except Exception as e:
        ADMIN_IDS = []
        print(f"[⚠️] Error al cargar admins: {e}")


def solo_admins(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = str(update.effective_user.id)
        if ADMIN_IDS and user_id not in ADMIN_IDS:
            await update.message.reply_text("🚫 Este comando es solo para administradores.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper


