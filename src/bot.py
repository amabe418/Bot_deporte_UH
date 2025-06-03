import json
import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    filters, ContextTypes, ConversationHandler, CallbackQueryHandler
)
from telegram.constants import ParseMode
from functools import wraps

#ADMIN
USERNAME_ADMIN = 'amabe003'

#region Datos
# Paths
current_dir = os.getcwd().removesuffix('src')
USUARIOS_FILE = current_dir + 'data/usuarios.json'
DEPORTES_FILE = current_dir + 'data/deportes.json'
PROFESORES_FILE = current_dir + 'data/profesores.json'
INSTALACIONES_FILE = current_dir + 'data/instalaciones.json'
ACTIVIDADES_FILE = current_dir + 'data/actividades.json'
# HORARIOS_FILE = 'data/horarios.json'

# Códigos para registro y edición
NOMBRE, CARRERA, AÑO, EDITAR_CARRERA, EDITAR_AÑO = range(5)
FIJAR_TITULO, FIJAR_UBICACION, FIJAR_INICIO, FIJAR_FIN, FIJAR_DESCRIPCION = range(5, 10)
PROFESOR_NOMBRE, PROFESOR_DEPORTE, PROFESOR_CONTACTO, PROFESOR_USUARIO = range(10, 14)

to_emoji = {
    "ajedrez": "\u265f",  # Chess pawn emoji
    "atletismo": "\u2754",  # White square emoji
    "baloncesto": "\u1f3c3",  # Basketball emoji
    "baseball": "\u1f3be",  # Baseball emoji
    "fútbol": "\u1f3cf",  # Soccer ball emoji
    "gimnasia musical aerobia": "\u1f4bb",  # Dancing woman emoji
    "judo": "\u1f93a",  # Karate emoji
    "kárate": "\u1f93a",  # Karate emoji
    "levantamiento de pesas": "\u274e",  # Pinch emoji
    "lucha": "\u275c",  # White triangle point right emoji
    "natación": "\u1f3ca",  # Swimming pool emoji
    "tenis de mesa": "\u1f3c8",  # Ping pong emoji
    "voleibol": "\u1f3d0"  # Volleyball emoji
}

# Utilidades JSON
def cargar_json(ruta):
    with open(ruta, 'r') as f:
        return json.load(f)

def guardar_json(ruta, datos):
    with open(ruta, 'w') as f:
        json.dump(datos, f, indent=4)

def guardar_actividades(actividades):
    guardar_json(ACTIVIDADES_FILE, actividades)

#region Metodos
# bot.py o utils.py
def solo_admin(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        print(f"USUARIO: !!!!{update.effective_user.username}")
        if update.effective_user.username != USERNAME_ADMIN:
            await update.message.reply_text("🚫 Este comando solo está disponible para el administrador.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper

def requiere_registro(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        username = update.effective_user.username
        usuarios = cargar_json(USUARIOS_FILE)
        if username not in usuarios:
            await update.message.reply_text("⚠️ Debes registrarte primero con /registro para usar esta función.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper


def solo_profesores(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        username = update.effective_user.username
        # Asegúrate de que 'usuarios' esté disponible en el módulo
        usuarios = cargar_json(USUARIOS_FILE)

        if usuarios[username]['tipo'] != 'profesor':
            await update.message.reply_text("🚫 Este comando solo está disponible para profesores.")
            return
        return await func(update, context, *args, **kwargs)

    return wrapper

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Bienvenido al bot deportivo de la Universidad de La Habana!\nEscribe /ayuda para más información."
    )

# /ayuda
async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/registrar - Registrarte como estudiante o profesor\n"
        "/perfil - Ver tu perfil registrado\n"
        "/editar_carrera - Cambiar carrera (solo estudiantes)\n"
        "/editar_anno - Cambiar año (solo estudiantes)\n"
        "/deportes - Listar deportes\n"
        "/profesores - Listar profesores\n"
        "/info_profesor <nombre> - Ver información de un profesor\n"
        "/instalaciones - Listar instalaciones\n"
        "/horarios - Mostrar horarios"
    )

# /registrar
async def registrar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usuarios = cargar_json(USUARIOS_FILE)
    username = update.effective_user.username

    if username in usuarios:
        await update.message.reply_text("Ya estás registrado.")
        return ConversationHandler.END

    await update.message.reply_text("¿Cuál es tu nombre real?", reply_markup=ReplyKeyboardRemove())
    return NOMBRE

async def recibir_nombre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["nombre"] = update.message.text
    await update.message.reply_text("¿Cuál es tu carrera?")
    return CARRERA

async def recibir_carrera(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["carrera"] = update.message.text
    await update.message.reply_text("¿Qué año cursas?")
    return AÑO

async def recibir_año(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["año"] = update.message.text
    return await guardar_usuario(update, context)

async def guardar_usuario(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.effective_user.username
    usuarios = cargar_json(USUARIOS_FILE)

    usuarios[username] = {
        "rol": "estudiante",
        "nombre": context.user_data["nombre"],
        "carrera": context.user_data["carrera"],
        "año": context.user_data["año"]
    }

    guardar_json(USUARIOS_FILE, usuarios)
    await update.message.reply_text("¡Registro completado con éxito!")
    return ConversationHandler.END

@solo_admin
async def registrar_profesor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Introduzca el nombre del profesor:")
    return PROFESOR_NOMBRE

async def recibir_profesor_nombre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["nombre"] = update.message.text
    await update.message.reply_text("¿Qué deporte imparte?")
    return PROFESOR_DEPORTE

async def recibir_profesor_deporte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["deporte"] = update.message.text
    await update.message.reply_text("¿Cuál es el número de contacto?")
    return PROFESOR_CONTACTO

async def recibir_profesor_contacto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["contacto"] = update.message.text
    await update.message.reply_text("Por favor, proporciona el nombre de usuario del profesor (sin @):")
    return PROFESOR_USUARIO

async def recibir_profesor_usuario(update: Update, context: ContextTypes.DEFAULT_TYPE):
    profesor_username = update.message.text.strip()
    usuarios = cargar_json(USUARIOS_FILE)

    if profesor_username in usuarios:
        await update.message.reply_text("Ese usuario ya está registrado.")
        return ConversationHandler.END

    usuarios[profesor_username] = {
        "rol": "profesor",
        "nombre": context.user_data["nombre"],
        "deporte": context.user_data["deporte"],
        "contacto": context.user_data["contacto"]
    }

    guardar_json(USUARIOS_FILE, usuarios)
    await update.message.reply_text("¡Profesor registrado con éxito!")
    return ConversationHandler.END

# /perfil
@requiere_registro
async def perfil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usuarios = cargar_json(USUARIOS_FILE)
    username = update.effective_user.username

    if username not in usuarios:
        await update.message.reply_text("No estás registrado. Usa /registrar primero.")
        return

    datos = usuarios[username]
    mensaje = f"👤 {datos['nombre']}\n🆔 Usuario: @{username}\n🎓 Rol: {datos['rol'].capitalize()}\n"
    if datos["rol"] == "estudiante":
        mensaje += f"📚 Carrera: {datos['carrera']}\n📅 Año: {datos['año']}"
    else:
        mensaje += f"🏢 Deporte: {datos['deporte']}\n📞 Contacto: {datos['contacto']}"
    await update.message.reply_text(mensaje)

# /editar_carrera
@requiere_registro
async def editar_carrera(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usuarios = cargar_json(USUARIOS_FILE)
    username = update.effective_user.username

    if username not in usuarios or usuarios[username]["rol"] != "estudiante":
        await update.message.reply_text("Esta opción solo está disponible para estudiantes.")
        return ConversationHandler.END

    await update.message.reply_text("Escribe tu nueva carrera:")
    return EDITAR_CARRERA

async def recibir_nueva_carrera(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nueva_carrera = update.message.text
    usuarios = cargar_json(USUARIOS_FILE)
    username = update.effective_user.username
    usuarios[username]["carrera"] = nueva_carrera
    guardar_json(USUARIOS_FILE, usuarios)
    await update.message.reply_text("Carrera actualizada.")
    return ConversationHandler.END

# /editar_año
@requiere_registro
async def editar_año(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usuarios = cargar_json(USUARIOS_FILE)
    username = update.effective_user.username

    if username not in usuarios or usuarios[username]["rol"] != "estudiante":
        await update.message.reply_text("Esta opción solo está disponible para estudiantes.")
        return ConversationHandler.END

    await update.message.reply_text("Escribe tu nuevo año:")
    return EDITAR_AÑO

async def recibir_nuevo_año(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nuevo_año = update.message.text.strip()
    usuarios = cargar_json(USUARIOS_FILE)
    username = update.effective_user.username

    if username not in usuarios or usuarios[username]["rol"] != "estudiante":
        await update.message.reply_text("Solo los estudiantes pueden editar el año.")
        return ConversationHandler.END

    carrera = usuarios[username].get("carrera", "").lower()

    if carrera != "Física":
        if not nuevo_año.isdigit():
            await update.message.reply_text("Por favor, introduce un número válido para el año.")
            return EDITAR_AÑO
        año_num = int(nuevo_año)
        if año_num < 1 or año_num > 4:
            await update.message.reply_text("El año debe estar entre 1 y 4 para tu carrera.")
            return EDITAR_AÑO

    usuarios[username]["año"] = nuevo_año
    guardar_json(USUARIOS_FILE, usuarios)
    await update.message.reply_text("Año actualizado.")
    return ConversationHandler.END

@requiere_registro
async def deportes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    deportes = cargar_json(DEPORTES_FILE)
    if not deportes:
        await update.message.reply_text("No hay deportes disponibles en este momento.")
        return

    keyboard = [
        [InlineKeyboardButton(d["nombre"], callback_data=f"deporte_{i}")]
        for i, d in enumerate(deportes)
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🏅 Selecciona un deporte:", reply_markup=reply_markup)
    context.user_data["deportes"] = deportes  # Guardamos los datos para usarlos en el callback

async def deporte_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    deportes = context.user_data.get("deportes", [])
    
    if data == "volver_deportes":
        # Volver a la lista
        keyboard = [
            [InlineKeyboardButton(d["nombre"], callback_data=f"deporte_{i}")]
            for i, d in enumerate(deportes)
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("🏅 Selecciona un deporte:", reply_markup=reply_markup)
    elif data.startswith("deporte_"):
        index = int(data.split("_")[1])
        d = deportes[index]
        mensaje = (
            f"<b>{d['nombre']}</b>\n"
            f"👨‍🏫 Profesor: {d['profesor']}\n"
            f"📞 Contacto: {d['contacto']}\n"
            f"📅 Día: {d['dia']}\n"
            f"🕓 Hora: {d['hora']}\n"
            f"📍 Lugar: {d['lugar']}"
        )
        keyboard = [[InlineKeyboardButton("🔙 Volver", callback_data="volver_deportes")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(mensaje, reply_markup=reply_markup, parse_mode=ParseMode.HTML)

@requiere_registro
async def profesores(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usuarios = cargar_json(USUARIOS_FILE)
    mensaje = ""
    print(usuarios.keys())
    for u in usuarios:
       print(usuarios[u])
       if usuarios[u]['rol'] == 'profesor':
        mensaje += (
            f"• {usuarios[u]['nombre']}\n"
            f" 📞 Contacto: {usuarios[u]['contacto']}\n"
            f" Disciplina: {usuarios[u]['deporte']}\n"
            f" 👤 Usuario: @{u}\n\n"
        )
    await update.message.reply_text("👨‍🏫 Profesores:\n\n" + mensaje)

@requiere_registro
async def info_profesor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre = " ".join(context.args)
    profesores = cargar_json(PROFESORES_FILE)
    for p in profesores:
        if p["nombre"].lower() == nombre.lower():
            mensaje = f"👤 Nombre: {p['nombre']}\n📍 Deporte: {p['deporte']}"
            await update.message.reply_text(mensaje)
            return
    await update.message.reply_text("Profesor no encontrado.")

@requiere_registro
@solo_profesores
async def fijar_actividad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usuarios = cargar_json(USUARIOS_FILE)
    username = update.effective_user.username

    if username not in usuarios or usuarios[username]["rol"] != "profesor":
        await update.message.reply_text("Solo los profesores pueden fijar actividades.")
        return ConversationHandler.END

    await update.message.reply_text("¿Cuál es el título de la actividad?")
    return FIJAR_TITULO

async def recibir_titulo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["titulo"] = update.message.text
    await update.message.reply_text("¿Dónde se realizará la actividad?")
    return FIJAR_UBICACION

async def recibir_ubicacion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["ubicacion"] = update.message.text
    await update.message.reply_text("¿Cuándo empieza? (formato: YYYY-MM-DD HH:MM)")
    return FIJAR_INICIO

async def recibir_inicio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    try:
        context.user_data["inicio"] = texto
        await update.message.reply_text("¿Cuándo termina? (formato: YYYY-MM-DD HH:MM)")
        return FIJAR_FIN
    except ValueError:
        await update.message.reply_text("Formato inválido. Usa YYYY-MM-DD HH:MM")
        return FIJAR_INICIO

async def recibir_fin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["fin"] = update.message.text
    await update.message.reply_text("Escribe una descripción (o escribe 'ninguna'):")
    return FIJAR_DESCRIPCION

async def recibir_descripcion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    descripcion = update.message.text
    if descripcion.lower() == "ninguna":
        descripcion = ""
    
    actividad = {
        "titulo": context.user_data["titulo"],
        "ubicacion": context.user_data["ubicacion"],
        "inicio": context.user_data["inicio"],
        "fin": context.user_data["fin"],
        "descripcion": descripcion,
        "profesor": f"@{update.effective_user.username}"
    }

    actividades = cargar_json(ACTIVIDADES_FILE)
    actividades.append(actividad)
    guardar_actividades(actividades)

    await update.message.reply_text("✅ Actividad registrada exitosamente.")
    return ConversationHandler.END

@requiere_registro
async def actividades(update: Update, context: ContextTypes.DEFAULT_TYPE):
    actividades = cargar_json(ACTIVIDADES_FILE)

    if not actividades:
        await update.message.reply_text("No hay actividades registradas en este momento.")
        return

    profesores = cargar_json(USUARIOS_FILE)
    mensaje = "📋 <b>Actividades:</b>\n\n"
    for a in actividades:
        mensaje += (
            f"<b>{a['titulo']}</b>\n"
            f"📍 Ubicación: {a['ubicacion']}\n"
            f"🗓️ Inicio: {a['inicio']}\n"
            f"⏰ Fin: {a['fin']}\n"
        )
        if a.get("descripcion"):
            mensaje += f"📝 {a['descripcion']}\n"

        prof_usr = a['profesor']
        mensaje += f"👨‍🏫 Profesor: {profesores[prof_usr[1:]]['nombre']}.\n👤 Usuario: {prof_usr} \n📞 Contacto: {profesores[prof_usr[1:]]['contacto']}\n\n"
    

    await update.message.reply_text(mensaje, parse_mode=ParseMode.HTML)

@requiere_registro
async def instalaciones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    instalaciones = cargar_json(INSTALACIONES_FILE)
    mensaje = "\n".join(f"{i}." for i in instalaciones)
    await update.message.reply_text("🏟️ Instalaciones:\n\n" + mensaje)

@requiere_registro
async def horarios(update: Update, context: ContextTypes.DEFAULT_TYPE):
    horarios = cargar_json(HORARIOS_FILE)
    mensaje = "\n".join(f"{h['deporte']} - {h['hora']} en {h['lugar']}" for h in horarios)
    await update.message.reply_text("📅 Horarios:\n" + mensaje)


#region Principal
with open('token.txt') as file:
    TOKEN = file.read().strip()
    

registro_handler = ConversationHandler(
    entry_points=[CommandHandler("registrar", registrar)],
    states={
        NOMBRE: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_nombre)],
        CARRERA: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_carrera)],
        AÑO: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_año)],
    },
    fallbacks=[],
)

registrar_profesor_handler = ConversationHandler(
    entry_points=[CommandHandler("registrar_profesor", registrar_profesor)],
    states={
        PROFESOR_NOMBRE: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_profesor_nombre)],
        PROFESOR_DEPORTE: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_profesor_deporte)],
        PROFESOR_CONTACTO: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_profesor_contacto)],
        PROFESOR_USUARIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_profesor_usuario)]
    },
    fallbacks=[],
)

editar_handler = ConversationHandler(
    entry_points=[CommandHandler("editar_carrera", editar_carrera),
                    CommandHandler("editar_anno", editar_año)],
    states={
        EDITAR_CARRERA: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_nueva_carrera)],
        EDITAR_AÑO: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_nuevo_año)],
    },
    fallbacks=[],
)

fijar_actividad_handler = ConversationHandler(
    entry_points=[CommandHandler("fijar_actividad", fijar_actividad)],
    states={
        FIJAR_TITULO: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_titulo)],
        FIJAR_UBICACION: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_ubicacion)],
        FIJAR_INICIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_inicio)],
        FIJAR_FIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_fin)],
        FIJAR_DESCRIPCION: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_descripcion)],
    },
    fallbacks=[],
)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(fijar_actividad_handler)
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("ayuda", ayuda))
app.add_handler(CommandHandler("perfil", perfil))
app.add_handler(CommandHandler("deportes", deportes))
app.add_handler(CallbackQueryHandler(deporte_callback, pattern="^deporte_|^volver_deportes$"))
app.add_handler(CommandHandler("profesores", profesores))
app.add_handler(CommandHandler("info_profesor", info_profesor))
app.add_handler(CommandHandler("instalaciones", instalaciones))
app.add_handler(CommandHandler("horarios", horarios))
app.add_handler(fijar_actividad_handler)
app.add_handler(CommandHandler("actividades", actividades))
app.add_handler(registro_handler)
app.add_handler(registrar_profesor_handler)
app.add_handler(editar_handler)
app.run_polling()