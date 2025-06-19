# hupper -m bot.py
import json
from telegram import Update, InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes,CallbackQueryHandler
from telegram.helpers import escape_markdown


# Información sobre deportes

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
# instalaciones = [
#     "1. Tabloncillo Ramiro Valdés Daussa",
#     "2. Sala de deportes de combate",
#     "3. Laboratorio de cultura física",
#     "4. Cancha de usos múltiples (baloncesto, béisbol cinco, futbol sala, balonmano)",
#     "5. Piscina de 50 metros",
#     "6. Pista de atletismo",
#     "7. Campo de fútbol 11 y futbol rugby",
#     "8. Sala de gimnasia rítmica y artística",
#     "9. Sala de gimnasia musical aerobia",
#     "10. Área terapéutica de la cultura física",
#     "11. Cancha de frontenis",
#     "12. Campo de tiro",
#     "13. Cancha de voleibol de playa",
#     "14. Gimnasio biosaludable, sala de musculación",
#     "15. Escalada",
#     "16. Cátedra de ajedrez",
#     "17. Cátedra de deporte electrónico",
#     "18. Salón de conferencias Antonio Barroso",
#     "19. Sala de informática",
#     "20. Despachos (5)",
#     "21. Cátedras del personal docente investigador con baños (4)",
#     "22. Taquillas (4)",
#     "23. Carpintería (2)",
#     "24. Oficina administrativa",
#     "25. Almacenes (6)",
#     "26. Cafeterías (2)"
# ]

#informacion de los profesores

with open("BD/profesores.json","r",encoding="utf-8") as f:
    profesores_info = json.load(f)

#actividades
with open("BD/noticias.json","r",encoding="utf-8") as f:
    actividades = json.load(f)

with open("BD/deportes.json","r",encoding="utf-8") as f:
    deportes_info = json.load(f)


# region Datos
# Registro de usuarios
def cargar_usuarios():
    try:
        with open("BD/usuarios.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def guardar_usuarios(usuarios):
    with open("BD/usuarios.json", "w", encoding="utf-8") as f:
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
    
    # Guardar información básica del usuario
    usuarios[user_id] = {
        "nombre": nombre_completo,
        "username": user.username if user.username else "No disponible",
        "fecha_registro": str(update.message.date),
        "tipo": None,
        "info_adicional": {}
    }
    
    # Preguntar si es profesor o estudiante
    keyboard = [
        [InlineKeyboardButton("Profesor", callback_data=f"tipo_profesor_{user_id}")],
        [InlineKeyboardButton("Estudiante", callback_data=f"tipo_estudiante_{user_id}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Por favor, selecciona tu tipo de usuario:",
        reply_markup=reply_markup
    )

async def procesar_tipo_usuario(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data.split('_')
    tipo = data[1]
    user_id = data[2]
    
    if tipo == "profesor":
        usuarios[user_id]["tipo"] = "profesor"
        guardar_usuarios(usuarios)
        await query.edit_message_text(
            f"¡Gracias por registrarte! Has sido registrado como profesor."
        )
    elif tipo == "estudiante":
        usuarios[user_id]["tipo"] = "estudiante"
        await query.edit_message_text(
            "Por favor, envía tu carrera y año que cursas en el siguiente formato:\n"
            "/info_estudiante Carrera Año"
            "\nPor ejemplo: /info_estudiante Matemática 3"
        )

async def info_estudiante(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = str(user.id)
    
    if user_id not in usuarios or usuarios[user_id]["tipo"] != "estudiante":
        await update.message.reply_text(
            "Por favor, primero regístrate como estudiante usando el comando /registrar."
        )
        return
    
    if len(context.args) < 2:
        await update.message.reply_text(
            "Por favor, proporciona tu carrera y año en el formato:\n"
            "/info_estudiante Carrera Año"
        )
        return
    
    carrera = " ".join(context.args[:-1])
    año = context.args[-1]
    
    usuarios[user_id]["info_adicional"] = {
        "carrera": carrera,
        "año": año
    }
    
    guardar_usuarios(usuarios)
    
    await update.message.reply_text(
        f"¡Gracias! Has completado tu registro como estudiante de {carrera}, {año}° año."
    )

async def horario(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Los horarios aún no están disponibles, pero pronto lo estarán.")


#region DEPORTES

def generar_teclado_deportes(pagina: int, elementos_por_pagina: int = 5):
    deportes = list(deportes_info.keys())
    total_paginas = (len(deportes) + elementos_por_pagina - 1) // elementos_por_pagina

    inicio = pagina * elementos_por_pagina
    fin = inicio + elementos_por_pagina
    deportes_pagina = deportes[inicio:fin]

    # Botones para los deportes en esta página
    botones = [
        [InlineKeyboardButton(nombre, callback_data=f"deporte_{nombre}")]
        for nombre in deportes_pagina
    ]

    # Botones de navegación
    botones_navegacion = []
    if pagina > 0:
        botones_navegacion.append(InlineKeyboardButton("⬅️ Anterior", callback_data=f"pagina_deportes_{pagina - 1}"))
    if pagina < total_paginas - 1:
        botones_navegacion.append(InlineKeyboardButton("Siguiente ➡️", callback_data=f"pagina_deportes_{pagina + 1}"))

    if botones_navegacion:
        botones.append(botones_navegacion)

    return InlineKeyboardMarkup(botones)


async def listar_deportes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # mensaje = "📝 *CARTELERA DE ENTRENAMIENTO DEPORTIVO SEDER-UH 2025*\n\n"
    
    # for deporte in deportes:
    #     mensaje += f"*DEPORTE:* {deporte['nombre']}\n"
    #     mensaje += f"*PROFESOR:* {deporte['profesor']} {deporte['contacto']}\n"
    #     mensaje += f"*DÍA:* {deporte['dia']}\n"
    #     mensaje += f"*HORA:* {deporte['hora']}\n"
    #     mensaje += f"*LUGAR:* {deporte['lugar']}\n\n"
    
    # await update.message.reply_text(mensaje, parse_mode='Markdown')

    reply_markup = generar_teclado_deportes(pagina=0)

    # keyboard = [
    #     [InlineKeyboardButton(nombre, callback_data=f"deporte_{nombre}")] 
    #     for nombre in deportes_info.keys()
    # ]

    # reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Selecciona un deportes para ver más información:",
        reply_markup=reply_markup
    )


async def mostrar_info_deporte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "volver_deportes":
        return await listar_deportes_callback(update, context)

    nombre = query.data.removeprefix("deporte_")
    info = deportes_info.get(nombre)

    if info:
        profesor = escape_markdown(info.get("profesor", "No disponible"), version=2)
        contacto = escape_markdown(info.get("contacto", "No disponible"), version=2)
        dias = escape_markdown(info.get("dias","No disponible"),version =2)
        horarios = escape_markdown(info.get("horario", "No disponible"), version=2)
        nombre_escapado = escape_markdown(nombre, version=2)

        # Procesar los lugares, reemplazando '-' por 'No definido' y escapando cada uno
        lugares_raw = info.get("lugar", [])
        lugares = [escape_markdown(l if l != "-" else "No definido", version=2) for l in lugares_raw]
        lugares_str = ', '.join(lugares)

        mensaje = (
            f"🏅 *{nombre_escapado}*\n\n"
            f"👨‍🏫 *Profesor:* {profesor}\n"
            f"📞 *Contacto:* {contacto}\n"
            f"📅 *Dias:* {dias}\n"
            f"🕒 *Horarios:* {horarios}\n"
            f"📍 *Lugares:* {lugares_str}"
        )
    else:
        mensaje = escape_markdown(f"No hay información disponible para {nombre}.", version=2)

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Volver a la lista", callback_data="volver_deportes")]
    ])

    await query.edit_message_text(
        text=mensaje,
        reply_markup=reply_markup,
        parse_mode='MarkdownV2'
    )

async def listar_deportes_callback(update:Update,context:ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    pagina = context.user_data.get('pagina_deportes', 0)
    
    reply_markup = generar_teclado_deportes(pagina=pagina)
    # keyboard = [
    #     [InlineKeyboardButton(nombre_d, callback_data=f"deporte_{nombre_d}")]
    #     for nombre_d in deportes_info.keys()
    # ]

    # reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        "Selecciona un deporte para ver más información:",
        reply_markup=reply_markup
    )


async def cambiar_pagina_deportes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Extraer el número de página desde callback_data
    _, _, pagina_str = query.data.split('_')
    pagina = int(pagina_str)

    context.user_data['pagina_deportes'] = pagina

    reply_markup = generar_teclado_deportes(pagina=pagina)

    await query.edit_message_text(
        text="Selecciona un deporte para ver más información:",
        reply_markup=reply_markup
    )


#endregion

#region PROFESORES

def generar_teclado_profesores(pagina: int, elementos_por_pagina: int = 5):
    profesores = list(profesores_info.keys())
    total_paginas = (len(profesores) + elementos_por_pagina - 1) // elementos_por_pagina

    inicio = pagina * elementos_por_pagina
    fin = inicio + elementos_por_pagina
    profesores_pagina = profesores[inicio:fin]

    # Botones para los deportes en esta página
    botones = [
        [InlineKeyboardButton(nombre, callback_data=f"profesor_{nombre}")]
        for nombre in profesores_pagina
    ]

    # Botones de navegación
    botones_navegacion = []
    if pagina > 0:
        botones_navegacion.append(InlineKeyboardButton("⬅️ Anterior", callback_data=f"pagina_profesores_{pagina - 1}"))
    if pagina < total_paginas - 1:
        botones_navegacion.append(InlineKeyboardButton("Siguiente ➡️", callback_data=f"pagina_profesores_{pagina + 1}"))

    if botones_navegacion:
        botones.append(botones_navegacion)

    return InlineKeyboardMarkup(botones)


async def listar_profesores(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # mensaje = "👨‍🏫 *PERSONAL DOCENTE INVESTIGADOR (PDI)*\n\n"
    
    # for profesor in profesores:
    #     mensaje += f"{profesor}\n"
    
    # await update.message.reply_text(mensaje, parse_mode='Markdown')

  
    # keyboard = [
    #     [InlineKeyboardButton(nombre, callback_data=f"profesor_{nombre}")] 
    #     for nombre in profesores_info.keys()
    # ]

    #reply_markup = InlineKeyboardMarkup(keyboard)

    reply_markup = generar_teclado_profesores(pagina=0)

    await update.message.reply_text(
        "Selecciona un profesor para ver más información:",
        reply_markup=reply_markup
    )
    

async def mostrar_info_profesor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "volver_profesores":
        return await listar_profesores_callback(update, context)

    nombre = query.data.removeprefix("profesor_")
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

    pagina = context.user_data.get('pagina_profesores', 0)
    
    reply_markup = generar_teclado_profesores(pagina=pagina)

    # keyboard = [  
    #     [InlineKeyboardButton(nombre, callback_data=f"profesor_{nombre}")]
    #     for nombre in profesores_info.keys()
    # ]

    # reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        "Selecciona un profesor para ver más información:",
        reply_markup=reply_markup
    )


async def cambiar_pagina_profesores(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Extraer el número de página desde callback_data
    _, _, pagina_str = query.data.split('_')
    pagina = int(pagina_str)

    context.user_data['pagina_profesores'] = pagina

    reply_markup = generar_teclado_profesores(pagina=pagina)

    await query.edit_message_text(
        text="Selecciona un profesor para ver más información:",
        reply_markup=reply_markup
    )

#endregion


def cargar_instalaciones():
    with open("BD/instalaciones.json", "r", encoding="utf-8") as f:
        return json.load(f)

instalaciones = cargar_instalaciones()

async def listar_instalaciones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = "🏟️ *INSTALACIONES DEPORTIVAS*\n\n"
    
    for instalacion in instalaciones:
        mensaje += f"{instalacion}\n"
    
    await update.message.reply_text(mensaje, parse_mode='Markdown')



#region ACTIVIDADES
async def actividades(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton(deporte["nombre"], callback_data=f"actividad_{deporte['nombre']}")]
        for deporte in deportes_info
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🏅 Selecciona una actividad para ver detalles:",
        reply_markup=reply_markup
    )

async def mostrar_noticias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not actividades:
        await update.message.reply_text("No hay actividades disponibles en este momento.")
        return

    mensaje = "📰 *Noticias y Actividades Próximas:*\n\n"
    for noticia in actividades:
        mensaje += f"🔹 *{noticia['titulo']}* ({noticia['fecha']})\n"
        mensaje += f"{noticia['descripcion']}\n\n"

    await update.message.reply_text(mensaje, parse_mode="Markdown")


async def actividades_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton(deporte["nombre"], callback_data=f"actividad_{deporte['nombre']}")]
        for deporte in deportes_info
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text="🏅 Selecciona una actividad para ver detalles:",
        reply_markup=reply_markup
    )


#endregion

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


# endregion

# region Principal

TOKEN = ""
with open("token.txt", "r") as f:
    TOKEN = f.read().strip()

application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", welcome))
application.add_handler(CommandHandler("registrar", registrar))
application.add_handler(CommandHandler("info_estudiante", info_estudiante))
application.add_handler(CallbackQueryHandler(procesar_tipo_usuario, pattern=r"^tipo_"))
application.add_handler(CommandHandler("horario", horario))
application.add_handler(CommandHandler("listar_deportes", listar_deportes))
application.add_handler(CommandHandler("listar_profesores", listar_profesores))
application.add_handler(CommandHandler("listar_instalaciones", listar_instalaciones))
application.add_handler(CommandHandler("ayuda", ayuda))
application.add_handler(CommandHandler("actividades", mostrar_noticias))

application.add_handler(CallbackQueryHandler(mostrar_info_profesor,pattern="^profesor_"))
application.add_handler(CallbackQueryHandler(mostrar_info_deporte,pattern="^deporte_"))


application.add_handler(CallbackQueryHandler(listar_deportes_callback, pattern="^volver_deportes$"))
application.add_handler(CallbackQueryHandler(listar_profesores_callback, pattern="^volver_profesores$"))


application.add_handler(CallbackQueryHandler(cambiar_pagina_deportes, pattern="^pagina_deportes_"))
application.add_handler(CallbackQueryHandler(cambiar_pagina_profesores, pattern="^pagina_profesores_"))

application.run_polling(allowed_updates=Update.ALL_TYPES)


# endregion

# region Despliegue

#endregion