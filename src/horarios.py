

import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from usuarios import usuario_registrado

# Estructura de datos de horarios por día
HORARIOS_POR_DIA = {
    "LUNES": """📅 <b>LUNES</b>

🔫 <b>Tiro Deportivo (M y F)</b> - 9:30 a 15:00H
Profesor Julián Hernández Domínguez 
📞 58452671
🏟️ Campo de tiro del Coppelia

🥋 <b>Judo (M y F)</b> - 14:00 a 17:00H
Profesor Juan Larrude Cárdenas 
📞 58081119
🏟️ Sala judo Estadio universitario Juan Abrantes Fernández 

🏀 <b>Baloncesto 5vs5 y 3x3 (M y F)</b> - 14:00 a 17:00H
Profesor Abdel Carlos Santana Arrechera 
📞 5 8430871
Profesora Jacqueline Sansó Paneque 
📞 53875195
🏟️ Tabloncillo Ramiro Valdés Daussá""",

    "MARTES": """📅 <b>MARTES</b>

🔫 <b>Tiro Deportivo (M y F)</b> - 9:30 a 15:00H
Profesor Julián Hernández Domínguez 
📞 58452671
🏟️ Campo de tiro del Coppelia

⚽️ <b>Futsal (M y F)</b> - 13:00 a 17:00H
Profesor José Emilio Cuevas Chávez 
📞 54753187
Profesor Henrry Ordóñez Pedroso 
📞 5 3865784
También atiende los proyectos
🏟️ Tabloncillo Ramiro Valdés Daussá 

⚽️ <b>Fútbol 11</b> - 14:00 a 17:00H
Profesor Armando Najarro Pérez
📞 5 9745870
🏟️ Terreno de fútbol Estadio universitario Juan Abrantes Fernández""",

    "MIÉRCOLES": """📅 <b>MIÉRCOLES</b>

🔫 <b>Tiro Deportivo (M y F)</b> - 9:30 a 15:00H
Profesor Julián Hernández Domínguez 
📞 58452671
🏟️ Campo de tiro del Coppelia

🏀 <b>Baloncesto 5vs5 y 3x3 (M y F)</b> - 14:00 a 17:00H
Profesor Abdel Carlos Santana Arrechera 
📞 5 8430871
Profesora Jacqueline Sansó Paneque 
📞 53875195
🏟️ Tabloncillo Ramiro Valdés Daussá 

🏐 <b>Voleibol (M y F)</b> - 14:00 a 17:00H
Profesor Luis Martinez Delgado 
📞 5 3317557
🏟️ Tabloncillo Ramiro Valdés Daussá 

🥋 <b>Kárate (M y F)</b> - 14:00 a 17:00H
Profesor Humberto López Mora 
📞 5 5352277
🏟️ Sala de Judo Estadío Juan Abrantes Fernández 

⚾️ <b>Béisbol 5 (Mixto)</b> - 14:00 a 17:00H
Profesor Luis Gustavo Lemagne Sánchez 
📞 5 6473537
🏟️ Terreno cemento

♟️ <b>Ajedrez (M y F)</b> - 14:00 a 17:00H
Profesora Cristina Rafoso Mendiondo 
📞 54822669
🏟️ Sala de ajedrez José Raúl Capablanca Estado Juan Abrantes Fernández""",

    "JUEVES": """📅 <b>JUEVES</b>

🔫 <b>Tiro Deportivo (M y F)</b> - 9:30 a 15:00H
Profesor Julián Hernández Domínguez 
📞 58452671
🏟️ Campo de tiro del Coppelia

⚽️ <b>Fútbol 11</b> - 14:00 a 17:00H
Profesor Armando Najarro Pérez
📞 5 9745870
🏟️ Terreno de fútbol Estadio universitario Juan Abrantes Fernández""",

    "VIERNES": """📅 <b>VIERNES</b>

🔫 <b>Tiro Deportivo (M y F)</b> - 9:30 a 15:00H
Profesor Julián Hernández Domínguez 
📞 58452671
🏟️ Campo de tiro del Coppelia

⚽️ <b>Futsal (M y F)</b> - 13:00 a 17:00H
Profesor José Emilio Cuevas Chávez 
📞 54753187
Profesor Henrry Ordóñez Pedroso 
📞 5 3865784
También atiende los proyectos
🏟️ Tabloncillo Ramiro Valdés Daussá""",

    "SÁBADO": """📅 <b>SÁBADOS</b>

🏸 <b>Bádminton (M y F)</b> - 9:00 a 12:00H
(Segundo y cuarto sábado de cada mes)
🏟️ Tabloncillo Ramiro Valdés Daussá 

⚽️ <b>Futsal (M y F)</b> - Concentrado
Profesor José Emilio Cuevas Chávez 
📞 54753187
Profesor Henrry Ordóñez Pedroso 
📞 5 3865784
🏟️ Tabloncillo Ramiro Valdés Daussá"""
}

@usuario_registrado
async def horario(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = """📅 <b>Entrenamiento deportivo en el SEDER</b>
<b>Curso académico 2025-2026</b>
<b>Fecha de inicio: 15/9.</b>

🗓️ <b>Selecciona un día para ver los horarios:</b>"""

    # Crear botones para cada día
    keyboard = [
        [InlineKeyboardButton("📅 Lunes", callback_data="horario_LUNES")],
        [InlineKeyboardButton("📅 Martes", callback_data="horario_MARTES")],
        [InlineKeyboardButton("📅 Miércoles", callback_data="horario_MIÉRCOLES")],
        [InlineKeyboardButton("📅 Jueves", callback_data="horario_JUEVES")],
        [InlineKeyboardButton("📅 Viernes", callback_data="horario_VIERNES")],
        [InlineKeyboardButton("📅 Sábado", callback_data="horario_SÁBADO")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(mensaje, parse_mode="HTML", reply_markup=reply_markup)


@usuario_registrado
async def mostrar_horario_dia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Extraer el día del callback_data (formato: "horario_DIA")
    dia = query.data.split("_", 1)[1] if "_" in query.data else None

    if dia and dia in HORARIOS_POR_DIA:
        horario_texto = HORARIOS_POR_DIA[dia]
        
        # Botón para volver al menú de días
        keyboard = [
            [InlineKeyboardButton("🔙 Volver a días", callback_data="volver_horarios")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text=horario_texto,
            parse_mode="HTML",
            reply_markup=reply_markup
        )
    else:
        await query.answer("❌ Día no encontrado", show_alert=True)


@usuario_registrado
async def volver_horarios(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    mensaje = """📅 <b>Entrenamiento deportivo en el SEDER</b>
<b>Curso académico 2025-2026</b>
<b>Fecha de inicio: 15/9.</b>

🗓️ <b>Selecciona un día para ver los horarios:</b>"""

    # Crear botones para cada día
    keyboard = [
        [InlineKeyboardButton("📅 Lunes", callback_data="horario_LUNES")],
        [InlineKeyboardButton("📅 Martes", callback_data="horario_MARTES")],
        [InlineKeyboardButton("📅 Miércoles", callback_data="horario_MIÉRCOLES")],
        [InlineKeyboardButton("📅 Jueves", callback_data="horario_JUEVES")],
        [InlineKeyboardButton("📅 Viernes", callback_data="horario_VIERNES")],
        [InlineKeyboardButton("📅 Sábado", callback_data="horario_SÁBADO")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=mensaje,
        parse_mode="HTML",
        reply_markup=reply_markup
    )
