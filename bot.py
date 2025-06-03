# hupper -m bot.py
import json
from telegram import Update, InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes,CallbackQueryHandler
from telegram.helpers import escape_markdown

# region Datos
# Información sobre deportes
deportes = [
    {"nombre": "Ajedrez", "profesor": "Cristina Raboso", "contacto": "54482669", "dia": "Todos los días", "hora": "Horario mañana/tarde", "lugar": "-"},
    {"nombre": "Atletismo", "profesor": "Carlos Miyares", "contacto": "51006637", "dia": "Martes y jueves", "hora": "A partir de las 3pm", "lugar": "Pista SEDER"},
    {"nombre": "Bádminton", "profesor": "Gisel Arrieta", "contacto": "53814079", "dia": "2do y 4to sábados de cada mes", "hora": "9:30 am a 12:30 pm", "lugar": "Tabloncillo Valdés Daussá"},
    {"nombre": "Baloncesto 5x5", "profesor": "Jacquelin Sansó", "contacto": "53875195", "dia": "Lunes y jueves", "hora": "1:30 pm a 6 pm", "lugar": "Tabloncillo Valdés Daussá"},
    {"nombre": "Baloncesto 3x3", "profesor": "Abdel Carlos Santana", "contacto": "58430871", "dia": "Lunes y jueves", "hora": "1:30 pm a 6 pm", "lugar": "Tabloncillo Valdés Daussá"},
    {"nombre": "Beisbol", "profesor": "No tenemos profesor", "contacto": "-", "dia": "-", "hora": "-", "lugar": "-"},
    {"nombre": "Beisbol 5", "profesor": "Profesor enfermo", "contacto": "-", "dia": "-", "hora": "-", "lugar": "-"},
    {"nombre": "Futbol 11", "profesor": "Henry Ordoñez y Armando Najarro", "contacto": "53865784", "dia": "Martes y jueves", "hora": "3 pm", "lugar": "Terreno de fútbol"},
    {"nombre": "Futsal (M-F)", "profesor": "José E. Cuevas", "contacto": "54753187", "dia": "Martes y viernes", "hora": "1 a 3 pm y 3 a 5 pm", "lugar": "Tabloncillo Valdés Daussá"},
    {"nombre": "GMA", "profesor": "Gisel Arrieta", "contacto": "53814079", "dia": "Jueves", "hora": "2 pm a 4 pm", "lugar": "Colchón de judo"},
    {"nombre": "Judo", "profesor": "Juan Antonio Larrude", "contacto": "58081119", "dia": "Lunes y miércoles", "hora": "2 pm a 5 pm", "lugar": "Colchón de judo"},
    {"nombre": "Kárate-TKVV", "profesor": "Humberto López y Victor", "contacto": "-", "dia": "Martes", "hora": "2 pm a 5 pm", "lugar": "Colchón de judo"},
    {"nombre": "Tiro Deportivo", "profesor": "Julián Hernández", "contacto": "58452671", "dia": "Lunes", "hora": "1:30-2:30 pm", "lugar": "Campo de tiro"},
    {"nombre": "Voleibol Sala (F-M)", "profesor": "Luis Martínez", "contacto": "53317557", "dia": "Miércoles", "hora": "2 a 3 pm y 3 a 4 pm", "lugar": "Tabloncillo Valdés Daussá"},
    {"nombre": "Voleibol Playa", "profesor": "Luis O. Pedraza", "contacto": "54226189", "dia": "Miércoles", "hora": "2 a 3 pm", "lugar": "-"}
]

# Lista de profesores
profesores = [
    "1. Abdel Carlos Santana Arrechea",
    "2. Armando Najarro Pérez",
    "3. Arnaldo Garbey Pascual",
    "4. Ana Karla Nuñez Nuñez",
    "5. Bárbara Dubé Sánchez",
    "6. Carlos Mateo Miyares Guirola",
    "7. Delia María Chappottín Salazar",
    "8. Gisel Arrieta Pérez",
    "9. Henry Ordoñez Pedroso",
    "10. Humberto López Mora",
    "11. Jacqueline Sanso Paneque",
    "12. José Antonio Pérez Amorós",
    "13. José Emilio Cuevas Chávez",
    "14. Juan Antonio Larrude Cárdenas",
    "15. Juan Royland Couret Ferrer",
    "16. Julian Hernández Dominguez",
    "17. Luis Martínez Delgado",
    "18. Luis Orlando Pedraza Dubernal",
    "19. María Cristina Rafoso Mendiondo",
    "20. Rebeca Garcia Nasser"
]

# Lista de instalaciones
instalaciones = [
    "1. Tabloncillo Ramiro Valdés Daussa",
    "2. Sala de deportes de combate",
    "3. Laboratorio de cultura física",
    "4. Cancha de usos múltiples (baloncesto, béisbol cinco, futbol sala, balonmano)",
    "5. Piscina de 50 metros",
    "6. Pista de atletismo",
    "7. Campo de fútbol 11 y futbol rugby",
    "8. Sala de gimnasia rítmica y artística",
    "9. Sala de gimnasia musical aerobia",
    "10. Área terapéutica de la cultura física",
    "11. Cancha de frontenis",
    "12. Campo de tiro",
    "13. Cancha de voleibol de playa",
    "14. Gimnasio biosaludable, sala de musculación",
    "15. Escalada",
    "16. Cátedra de ajedrez",
    "17. Cátedra de deporte electrónico",
    "18. Salón de conferencias Antonio Barroso",
    "19. Sala de informática",
    "20. Despachos (5)",
    "21. Cátedras del personal docente investigador con baños (4)",
    "22. Taquillas (4)",
    "23. Carpintería (2)",
    "24. Oficina administrativa",
    "25. Almacenes (6)",
    "26. Cafeterías (2)"
]

#informacion de los profesores

with open("profesores.json","r",encoding="utf-8") as f:
    profesores_info = json.load(f)

# region Datos
# Registro de usuarios
def cargar_usuarios():
    try:
        with open("usuarios.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def guardar_usuarios(usuarios):
    with open("usuarios.json", "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)

usuarios = cargar_usuarios()

# endregion

# region Metodos
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = str(user.id)
    
    if user_id not in usuarios:
        # Enviar mensaje solicitando nombre y apellido
        await update.message.reply_text(
            "¡Bienvenido! Para registrarte, por favor envía tu nombre y apellido en el siguiente formato:\n"
            "/registrar Nombre Apellido"
        )
    else:
        await update.message.reply_text(
            f"¡Hola {usuarios[user_id]['nombre']}, bienvenido de nuevo al bot de deportes de la Universidad de la Habana!"
        )

async def registrar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = str(user.id)
    
    # Verificar si se proporcionó el nombre y apellido
    if len(context.args) < 2:
        await update.message.reply_text(
            "Por favor, proporciona tu nombre y apellido en el formato:\n"
            "/registrar Nombre Apellido"
        )
        return
    
    # Obtener nombre y apellido del comando
    nombre_completo = " ".join(context.args)
    
    # Guardar información del usuario
    usuarios[user_id] = {
        "nombre": nombre_completo,
        "username": user.username if user.username else "No disponible",
        "fecha_registro": str(update.message.date)
    }
    
    # Guardar en el archivo
    guardar_usuarios(usuarios)
    
    await update.message.reply_text(
        f"¡Gracias por registrarte, {nombre_completo}! Ya puedes usar todos los servicios del bot."
    )

async def horario(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Los horarios aún no están disponibles, pero pronto lo estarán.")

async def listar_deportes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = "📝 *CARTELERA DE ENTRENAMIENTO DEPORTIVO SEDER-UH 2025*\n\n"
    
    for deporte in deportes:
        mensaje += f"*DEPORTE:* {deporte['nombre']}\n"
        mensaje += f"*PROFESOR:* {deporte['profesor']} {deporte['contacto']}\n"
        mensaje += f"*DÍA:* {deporte['dia']}\n"
        mensaje += f"*HORA:* {deporte['hora']}\n"
        mensaje += f"*LUGAR:* {deporte['lugar']}\n\n"
    
    await update.message.reply_text(mensaje, parse_mode='Markdown')

async def listar_profesores(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # mensaje = "👨‍🏫 *PERSONAL DOCENTE INVESTIGADOR (PDI)*\n\n"
    
    # for profesor in profesores:
    #     mensaje += f"{profesor}\n"
    
    # await update.message.reply_text(mensaje, parse_mode='Markdown')

  
    keyboard = [
        [InlineKeyboardButton(nombre, callback_data=nombre)] 
        for nombre in profesores_info.keys()
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Selecciona un profesor para ver más información:",
        reply_markup=reply_markup
    )
    

async def mostrar_info_profesor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "volver_profesores":
        return await listar_profesores_callback(update, context)

    nombre = query.data
    info = profesores_info.get(nombre)

    if info:
        deportes = escape_markdown(', '.join(info.get("deportes", [])), version=2)
        contacto = escape_markdown(info.get("contacto", "No disponible"), version=2)
        horarios = escape_markdown(info.get("horarios", "No disponible"), version=2)
        nombre_escapado = escape_markdown(nombre, version=2)

        # Procesar los lugares, reemplazando '-' por 'No definido' y escapando cada uno
        lugares_raw = info.get("lugares", [])
        lugares = [escape_markdown(l if l != "-" else "No definido", version=2) for l in lugares_raw]
        lugares_str = ', '.join(lugares)

        mensaje = (
            f"👨‍🏫 *{nombre_escapado}*\n\n"
            f"🏅 *Deportes:* {deportes}\n"
            f"📞 *Contacto:* {contacto}\n"
            f"🕒 *Horarios:* {horarios}\n"
            f"📍 *Lugares:* {lugares_str}"
        )
    else:
        mensaje = escape_markdown(f"No hay información disponible para {nombre}.", version=2)

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Volver a la lista", callback_data="volver_profesores")]
    ])

    await query.edit_message_text(
        text=mensaje,
        reply_markup=reply_markup,
        parse_mode='MarkdownV2'
    )


async def listar_profesores_callback(update:Update,context:ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(nombre, callback_data=nombre)]
        for nombre in profesores_info.keys()
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        "Selecciona un profesor para ver más información:",
        reply_markup=reply_markup
    )

async def listar_instalaciones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = "🏟️ *INSTALACIONES DEPORTIVAS*\n\n"
    
    for instalacion in instalaciones:
        mensaje += f"{instalacion}\n"
    
    await update.message.reply_text(mensaje, parse_mode='Markdown')


async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = "📋 *Comandos disponibles:*\n\n"
    mensaje += "/start - Bienvenida al bot\n"
    mensaje += "/horario - Consultar horarios\n"
    mensaje += "/listar_deportes - Ver la lista de deportes disponibles\n"
    mensaje += "/listar_profesores - Ver la lista de profesores\n"
    mensaje += "/listar_instalaciones - Ver la lista de instalaciones deportivas\n"
    mensaje += "/ayuda - Mostrar esta lista de comandos\n"

    mensaje = mensaje.replace("-", "\\-").replace(".", "\\.").replace("(", "\\(").replace(")", "\\)").replace("_", "\\_")

    await update.message.reply_text(mensaje, parse_mode='MarkdownV2')


# endregion

# region Principal

TOKEN = ""
with open("token.txt", "r") as f:
    TOKEN = f.read().strip()

application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", welcome))
application.add_handler(CommandHandler("registrar", registrar))
application.add_handler(CommandHandler("horario", horario))
application.add_handler(CommandHandler("listar_deportes", listar_deportes))
application.add_handler(CommandHandler("listar_profesores", listar_profesores))
application.add_handler(CommandHandler("listar_instalaciones", listar_instalaciones))
application.add_handler(CommandHandler("ayuda", ayuda))
application.add_handler(CallbackQueryHandler(mostrar_info_profesor))
application.run_polling(allowed_updates=Update.ALL_TYPES)
# endregion

# region Despliegue

#endregion