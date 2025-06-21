

from telegram import Update, InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes,CallbackQueryHandler,MessageHandler,filters
import usuarios
import deporte
import profesores
import instalaciones
import horarios
import actividades
import ayuda
import admin

actividades.cargar_actividades()
deporte.cargar_deportes()
instalaciones.cargar_instalaciones()  

profesores.cargar_profesores()
usuarios.cargar_usuarios()

admin.cargar_admins()

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = str(user.id)

    if user_id not in usuarios.usuarios:
        usuarios.registro_estado[user_id] = "esperando_nombre"
        await update.message.reply_text(
            "👋 <b>¡Bienvenido al Bot Deportivo de la Universidad de La Habana!</b>\n\n"
            "🔐 Para comenzar, necesitamos algunos datos.\n\n"
            "📝 ¿Cuál es tu <b>nombre completo</b>?",
            parse_mode="HTML"
        )
    else:
        msg = (
            f"🙌 <b>¡Hola {usuarios.usuarios[user_id]['nombre']}!</b>\n\n"
            "🏟️ Bienvenido de nuevo al Bot de Deportes de la Universidad de La Habana.\n"
            "Explora actividades, entrenamientos y más. 🏀🏐🏊"
        )

        if admin.ADMIN_IDS and user_id in admin.ADMIN_IDS:
            teclado = [
                [InlineKeyboardButton("➕ Agregar nuevo deporte", callback_data="admin_agregar_deporte")],
                [InlineKeyboardButton("➕ Agregar nuevo profesor", callback_data="admin_agregar_profesor")],
            ]
            await update.message.reply_text(
                msg,
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup(teclado)
            )
        else:
            await update.message.reply_text(
                msg,
                parse_mode="HTML"
            )



TOKEN = ""
with open("../token.txt", "r") as f:
    TOKEN = f.read().strip()


async def manejar_texto_privado(update, context):
    user_id = str(update.effective_user.id)

    if user_id in usuarios.registro_estado:
        await usuarios.manejar_respuesta_registro(update, context)
    elif user_id in deporte.deporte_estado:
        await deporte.manejar_respuesta_deporte(update, context)
    elif user_id in profesores.profesores_estado:
        await profesores.manejar_respuesta_profesores(update, context)
    else:
        await update.message.reply_text("🤖 No estás en ningún flujo. Usa /registro o /agregardeporte.")

# Define tus filtros como clases



application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", welcome))
application.add_handler(CommandHandler("registrar", usuarios.registro))
application.add_handler(
    CallbackQueryHandler(deporte.registro_deporte, pattern="^admin_agregar_deporte$")
)
application.add_handler(
    CallbackQueryHandler(profesores.registro_profesores, pattern="^admin_agregar_profesor$")
)



application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND & filters.ChatType.PRIVATE,
        manejar_texto_privado
    ))

application.add_handler(CallbackQueryHandler(usuarios.manejar_tipo_callback, pattern="^tipo_"))
application.add_handler(CallbackQueryHandler(deporte.manejar_confirmacion_deporte, pattern="^confirmar_deporte|cancelar_deporte$"))
application.add_handler(CallbackQueryHandler(profesores.manejar_confirmacion_profesores, pattern="^confirmar_profesor|cancelar_profesor$"))


# application.add_handler(CommandHandler("registrar", registrar))
# application.add_handler(CommandHandler("info_estudiante", info_estudiante))
# application.add_handler(CallbackQueryHandler(procesar_tipo_usuario, pattern=r"^tipo_"))
application.add_handler(CommandHandler("horario", horarios.horario))
application.add_handler(CommandHandler("listar_deportes", deporte.listar_deportes))
application.add_handler(CommandHandler("listar_profesores", profesores.listar_profesores))
application.add_handler(CommandHandler("listar_instalaciones", instalaciones.listar_instalaciones))
application.add_handler(CommandHandler("ayuda", ayuda.ayuda))
application.add_handler(CommandHandler("actividades", actividades.mostrar_noticias))

application.add_handler(CallbackQueryHandler(profesores.mostrar_info_profesor,pattern="^profesor_"))
application.add_handler(CallbackQueryHandler(deporte.mostrar_info_deporte,pattern="^deporte_"))


application.add_handler(CallbackQueryHandler(deporte.listar_deportes_callback, pattern="^volver_deportes$"))
application.add_handler(CallbackQueryHandler(profesores.listar_profesores_callback, pattern="^volver_profesores$"))


application.add_handler(CallbackQueryHandler(deporte.cambiar_pagina_deportes, pattern="^pagina_deportes_"))
application.add_handler(CallbackQueryHandler(profesores.cambiar_pagina_profesores, pattern="^pagina_profesores_"))

#ADMIN
# application.add_handler(CommandHandler("agregar_deporte", agregar_deporte))
# application.add_handler(CommandHandler("agregar_profesor", agregar_profesor))
# application.add_handler(CallbackQueryHandler(admin_callback_handler, pattern="^(agregar_deporte|agregar_profesor)$"))



application.run_polling(allowed_updates=Update.ALL_TYPES)
