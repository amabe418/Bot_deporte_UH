# hupper -m bot.py
import json
from telegram import Update, InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes,CallbackQueryHandler,MessageHandler,filters
from telegram.helpers import escape_markdown
from functools import wraps
from datetime import datetime
# Información sobre deportes

# Estados posibles (constantes)
(
    ESTADO_REGISTRO_NOMBRE,
    ESTADO_REGISTRO_TIPO,
    ESTADO_REGISTRO_CARRERA,
    ESTADO_REGISTRO_AÑO,
    ESTADO_DEPORTE_NOMBRE,
    ESTADO_DEPORTE_PROFESOR,
    ESTADO_DEPORTE_CONTACTO,
    ESTADO_DEPORTE_DIAS,
    ESTADO_DEPORTE_HORARIO,
    ESTADO_DEPORTE_LUGARES
) = range(10)  # Asigna números únicos a cada estado


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



def cargar_admins():
    with open("BD/admins.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        return set(data["admins"])  # usar set para búsquedas rápidas

ADMIN_IDS = cargar_admins()

def usuario_registrado(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = str(update.effective_user.id)
        if user_id not in usuarios:
            await update.message.reply_text("🚫 Debes registrarte antes de usar este comando.")
            return
        return await func(update, context)
    return wrapper



def solo_admins(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = str(update.effective_user.id)
        if user_id not in ADMIN_IDS:
            await update.message.reply_text("🚫 Este comando es solo para administradores.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper


# endregion

#region ADMIN
registro_estado = {}
admin_add_state = {}

@solo_admins
async def agregar_deporte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # user_id = str(update.effective_user.id)
    # admin_add_state[user_id] = "esperando_nombre_deporte"
    # context.user_data.clear()  # Limpia cualquier info previa

    # if update.callback_query:
    #     await update.callback_query.edit_message_text("📥 Envíame el nombre del nuevo deporte:")
    # else:
    #     await update.message.reply_text("📥 Envíame el nombre del nuevo deporte:")

        """Inicia el flujo para agregar deporte (solo admin)"""
        
        context.user_data.clear()
        context.user_data['estado'] = ESTADO_DEPORTE_NOMBRE
        await update.message.reply_text("📥 Envíame el nombre del nuevo deporte:")



async def manejar_todos_los_mensajes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler único para todos los mensajes de texto"""
    estado_actual = context.user_data.get('estado')
    texto = update.message.text.strip()

    if estado_actual == ESTADO_REGISTRO_NOMBRE:
        context.user_data['nombre'] = texto
        context.user_data['estado'] = ESTADO_REGISTRO_TIPO
        
        keyboard = [
            [InlineKeyboardButton("Profesor", callback_data="tipo_profesor")],
            [InlineKeyboardButton("Estudiante", callback_data="tipo_estudiante")]
        ]
        await update.message.reply_text(
            "¿Eres profesor o estudiante?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif estado_actual == ESTADO_REGISTRO_CARRERA:
        context.user_data['carrera'] = texto
        context.user_data['estado'] = ESTADO_REGISTRO_AÑO
        await update.message.reply_text("¿Qué año cursas?")

    elif estado_actual == ESTADO_REGISTRO_AÑO:
        context.user_data['año'] = texto
        await guardar_usuario_completo(update, context)
        await update.message.reply_text("✅ ¡Registro completado con éxito!")
        context.user_data.clear()

    elif estado_actual == ESTADO_DEPORTE_NOMBRE:
        context.user_data['nombre_deporte'] = texto
        context.user_data['estado'] = ESTADO_DEPORTE_PROFESOR
        await update.message.reply_text("👨‍🏫 ¿Cuál es el nombre del profesor?")

    elif estado_actual == ESTADO_DEPORTE_PROFESOR:
        context.user_data['profesor_deporte'] = texto
        context.user_data['estado'] = ESTADO_DEPORTE_CONTACTO
        await update.message.reply_text("📞 ¿Cuál es el contacto del profesor?")

    elif estado_actual ==  ESTADO_DEPORTE_CONTACTO:
        context.user_data['contacto_deporte']= texto
        context.user_data['estado'] = ESTADO_DEPORTE_DIAS
        await update.message.reply_text("📅 ¿Qué días se dicta este deporte?")
    
    elif estado_actual ==  ESTADO_DEPORTE_DIAS:
        context.user_data['dias_deporte']= texto
        context.user_data['estado'] = ESTADO_DEPORTE_HORARIO
        await update.message.reply_text("⏰ ¿Cuál es el horario?")

    elif estado_actual ==  ESTADO_DEPORTE_HORARIO:
        context.user_data['dias_deporte']= texto
        context.user_data['estado'] = ESTADO_DEPORTE_LUGARES
        await update.message.reply_text("📍 ¿En qué lugar(es) se practica? (separa con comas)")
        
    elif estado_actual == ESTADO_DEPORTE_LUGARES:
        lugares = [l.strip() for l in texto.split(",")]
        context.user_data['lugares_deporte'] = lugares
        await guardar_deporte(context.user_data)
        await update.message.reply_text("✅ ¡Deporte agregado exitosamente!")
        context.user_data.clear()


async def manejar_tipo_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja la selección de tipo (profesor/estudiante)"""
    query = update.callback_query
    await query.answer()
    
    tipo = query.data.split("_")[1]
    context.user_data['tipo'] = tipo

    if tipo == "profesor":
        await guardar_usuario_completo(update, context)
        await query.edit_message_text("¡Gracias! Has sido registrado como profesor.")
    else:
        context.user_data['estado'] = ESTADO_REGISTRO_CARRERA
        await query.edit_message_text("¿Cuál es tu carrera?")

# async def manejar_respuesta_agregar_deporte(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user_id = str(update.effective_user.id)
#     if user_id not in admin_add_state:
#         return

#     estado = admin_add_state[user_id]
#     texto = update.message.text.strip()

#     if estado == "esperando_nombre_deporte":
#         # Guarda nombre en context.user_data
#         context.user_data["nombre_deporte"] = texto
#         admin_add_state[user_id] = "esperando_profesor_deporte"

#         # Preguntar quién será el profesor
#         await update.message.reply_text("👨‍🏫 ¿Cuál es el nombre del profesor para este deporte?")

#     elif estado == "esperando_profesor_deporte":
#         context.user_data["profesor_deporte"] = texto
#         admin_add_state[user_id] = "esperando_contacto_deporte"

#         await update.message.reply_text("📞 ¿Cuál es el contacto del profesor?")

#     elif estado == "esperando_contacto_deporte":
#         context.user_data["contacto_deporte"] = texto
#         admin_add_state[user_id] = "esperando_dias_deporte"

#         await update.message.reply_text("📅 ¿Qué días se dicta este deporte?")

#     elif estado == "esperando_dias_deporte":
#         context.user_data["dias_deporte"] = texto
#         admin_add_state[user_id] = "esperando_horario_deporte"

#         await update.message.reply_text("⏰ ¿Cuál es el horario?")

#     elif estado == "esperando_horario_deporte":
#         context.user_data["horario_deporte"] = texto
#         admin_add_state[user_id] = "esperando_lugares_deporte"

#         await update.message.reply_text("📍 ¿En qué lugar(es) se practica? (separa con comas)")

#     elif estado == "esperando_lugares_deporte":
#         lugares = [lugar.strip() for lugar in texto.split(",")]
#         context.user_data["lugares_deporte"] = lugares

#         # Guardar en deportes.json
#         await guardar_deporte(context.user_data)
#         del admin_add_state[user_id]
#         await update.message.reply_text("✅ ¡Deporte agregado exitosamente!")

#         # Limpiar estado
#         admin_add_state.pop(user_id)
#         context.user_data.clear()


async def guardar_deporte(data):
    # Leer archivo
    with open("deportes.json", "r", encoding="utf-8") as f:
        deportes = json.load(f)

    nombre = data["nombre_deporte"]

    deportes[nombre] = {
        "profesor": data["profesor_deporte"],
        "contacto": data["contacto_deporte"],
        "dias": data["dias_deporte"],
        "horario": data["horario_deporte"],
        "lugar": data["lugares_deporte"]
    }

    # Guardar archivo
    with open("deportes.json", "w", encoding="utf-8") as f:
        json.dump(deportes, f, indent=4, ensure_ascii=False)


@solo_admins
async def agregar_profesor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    if update.callback_query:
        await update.callback_query.edit_message_text("👨‍🏫 ¿Cuál es el nombre del nuevo profesor?")
    else:
        await update.message.reply_text("👨‍🏫 ¿Cuál es el nombre del nuevo profesor?")


# Este handler recibe la pulsación de botones y redirige a la función correcta
async def admin_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = str(query.from_user.id)
    await query.answer()  # Para que desaparezca el "reloj"

    if user_id not in ADMIN_IDS:
        await query.edit_message_text("🚫 Solo administradores pueden usar esto.")
        return

    if query.data == "agregar_deporte":
        await agregar_deporte(update, context)
    elif query.data == "agregar_profesor":
        await agregar_profesor(update, context)
    else:
        await query.edit_message_text("Opción no reconocida.")



#endregion



# region Metodos
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = str(user.id)

    if user_id not in usuarios:
        registro_estado[user_id] = "esperando_nombre"
        await update.message.reply_text(
            "👋 <b>¡Bienvenido al Bot Deportivo de la Universidad de La Habana!</b>\n\n"
            "🔐 Para comenzar, necesitamos algunos datos.\n\n"
            "📝 ¿Cuál es tu <b>nombre completo</b>?",
            parse_mode="HTML"
        )
    else:
        await update.message.reply_text(
            f"🙌 <b>¡Hola {usuarios[user_id]['nombre']}!</b>\n\n"
            "🏟️ Bienvenido de nuevo al Bot de Deportes de la Universidad de La Habana.\n"
            "Explora actividades, entrenamientos y más. 🏀🏐🏊",
            parse_mode="HTML"
        )
    

    if user_id in ADMIN_IDS:
        keyboard = [
            [InlineKeyboardButton("➕ Agregar Deporte", callback_data="agregar_deporte")],
            [InlineKeyboardButton("➕ Agregar Profesor", callback_data="agregar_profesor")],
            # Agrega más botones si quieres
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Bienvenido administrador, elige una acción:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("No eres admin, elige una acción:")

async def registro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    registro_estado[user_id] = "esperando_nombre"
    await update.message.reply_text("¿Cuál es tu nombre completo?")

# async def manejar_respuesta_registro(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user = update.message.from_user
#     user_id = str(user.id)
#     texto = update.message.text.strip()

#     if user_id not in registro_estado:
#         return

#     estado = registro_estado[user_id]

#     if estado == "esperando_nombre":
#         context.user_data["nombre"] = texto
#         registro_estado[user_id] = "esperando_tipo"
#         keyboard = [
#             [InlineKeyboardButton("Profesor", callback_data="tipo_profesor")],
#             [InlineKeyboardButton("Estudiante", callback_data="tipo_estudiante")]
#         ]
#         await update.message.reply_text("¿Eres profesor o estudiante?", reply_markup=InlineKeyboardMarkup(keyboard))

#     elif estado == "esperando_carrera":
#         context.user_data["carrera"] = texto
#         registro_estado[user_id] = "esperando_año"
#         await update.message.reply_text("¿Qué año cursas?")

#     elif estado == "esperando_año":
#         context.user_data["año"] = texto
#         guardar_usuario_completo(user_id, user.username, context)
#         del registro_estado[user_id]
#         await update.message.reply_text(
#             "✅ *¡Registro completado con éxito!*\n\n"
#             "Ya puedes comenzar a usar el bot y explorar las actividades deportivas 🏀🏐🏊",
#             parse_mode="Markdown"
#         )
#         del registro_estado[user_id]

async def manejar_tipo_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    tipo = query.data.split("_")[1]
    user_id = str(query.from_user.id)
    context.user_data["tipo"] = tipo

    if tipo == "profesor":
        guardar_usuario_completo(user_id, query.from_user.username, context)
        await query.edit_message_text("¡Gracias! Has sido registrado como profesor.")
        registro_estado.pop(user_id, None)
    else:
        registro_estado[user_id] = "esperando_carrera"
        await query.edit_message_text("¿Cuál es tu carrera?")

def guardar_usuario_completo(user_id, username, context):
    usuarios[user_id] = {
        "nombre": context.user_data.get("nombre", ""),
        "username": username if username else "No disponible",
        "fecha_registro": str(datetime.now()),
        "tipo": context.user_data.get("tipo", ""),
        "info_adicional": {
            "carrera": context.user_data.get("carrera", ""),
            "año": context.user_data.get("año", "")
        }
    }
    guardar_usuarios(usuarios)


@usuario_registrado
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

@usuario_registrado
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

@usuario_registrado
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

@usuario_registrado
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

@usuario_registrado
async def mostrar_noticias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not actividades:
        await update.message.reply_text("No hay actividades disponibles en este momento.")
        return

    mensaje = "📰 *Noticias y Actividades Próximas:*\n\n"
    for noticia in actividades:
        mensaje += f"🔹 *{noticia['titulo']}* ({noticia['fecha']})\n"
        mensaje += f"{noticia['descripcion']}\n\n"

    await update.message.reply_text(mensaje, parse_mode="Markdown")

@usuario_registrado
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


# endregion

# region Principal

TOKEN = ""
with open("token.txt", "r") as f:
    TOKEN = f.read().strip()

# Define tus filtros como clases



application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", welcome))
application.add_handler(CommandHandler("registrar", registro))


application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND & filters.ChatType.PRIVATE,
        manejar_todos_los_mensajes
    ))

application.add_handler(CallbackQueryHandler(manejar_tipo_callback, pattern="^tipo_"))


# application.add_handler(CommandHandler("registrar", registrar))
# application.add_handler(CommandHandler("info_estudiante", info_estudiante))
# application.add_handler(CallbackQueryHandler(procesar_tipo_usuario, pattern=r"^tipo_"))
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

#ADMIN
application.add_handler(CommandHandler("agregar_deporte", agregar_deporte))
application.add_handler(CommandHandler("agregar_profesor", agregar_profesor))
application.add_handler(CallbackQueryHandler(admin_callback_handler, pattern="^(agregar_deporte|agregar_profesor)$"))


application.run_polling(allowed_updates=Update.ALL_TYPES)


# endregion

# region Despliegue

#endregion