

from telegram import Update
from telegram.ext import ContextTypes
from usuarios import usuario_registrado



@usuario_registrado
async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = "📋 *Comandos disponibles:*\n\n"
    mensaje += "/start - Bienvenida al bot\n"
    mensaje += "/horario - Consultar horarios\n"
    mensaje += "/actividades - Ver menú de actividades deportivas\n"
    mensaje += "/listar_deportes - Ver la lista de deportes disponibles\n"
    mensaje += "/listar_profesores - Ver la lista de profesores\n"
    mensaje += "/listar_instalaciones - Ver la lista de instalaciones deportivas\n"
    mensaje += "/ayuda - Mostrar esta lista de comandos\n"

    mensaje = mensaje.replace("-", "\\-").replace(".", "\\.").replace("(", "\\(").replace(")", "\\)").replace("_", "\\_")

    await update.message.reply_text(mensaje, parse_mode='MarkdownV2')
