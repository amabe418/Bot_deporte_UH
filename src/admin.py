


import json
from telegram import Update
from telegram.ext import ContextTypes
from functools import wraps


ADMIN_IDS = []
admin_add_state = {}

def cargar_admins():
    global ADMIN_IDS
    try:
        with open("../BD/admins.json", "r", encoding="utf-8") as f:
            contenido = f.read().strip()
            if not contenido:
                ADMIN_IDS = []
            else:
                data = json.loads(contenido)
                ADMIN_IDS = data.get("admins", [])
    except FileNotFoundError:
        ADMIN_IDS = []
        print("[⚠️] Archivo admins.json no encontrado. Se creará cuando se registre el primer admin.")
    except json.JSONDecodeError as e:
        ADMIN_IDS = []
        print(f"[⚠️] Error al parsear admins.json: {e}. Se iniciará con lista vacía.")
    except Exception as e:
        ADMIN_IDS = []
        print(f"[⚠️] Error al cargar admins: {e}")


def solo_admins(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = str(update.effective_user.id)
        if ADMIN_IDS and user_id not in ADMIN_IDS:
            # Manejar tanto mensajes como callbacks
            if update.message:
                await update.message.reply_text("🚫 Este comando es solo para administradores.")
            elif update.callback_query:
                await update.callback_query.answer("🚫 Este comando es solo para administradores.", show_alert=True)
            return
        return await func(update, context, *args, **kwargs)
    return wrapper


