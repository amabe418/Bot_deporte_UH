

import json
from telegram import Update
from telegram.ext import ContextTypes
from usuarios import usuario_registrado

@usuario_registrado
async def horario(update: Update, context: ContextTypes.DEFAULT_TYPE):
    horarios_texto = """📅 <b>Entrenamiento deportivo en el SEDER</b>
<b>Curso académico 2025-2026</b>
<b>Fecha de inicio: 15/9.</b>

🗓️ <b>HORARIOS POR DÍAS</b>

📅 <b>LUNES</b>
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
🏟️ Tabloncillo Ramiro Valdés Daussá 

📅 <b>MARTES</b>
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
🏟️ Terreno de fútbol Estadio universitario Juan Abrantes Fernández 

📅 <b>MIÉRCOLES</b>
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
🏟️ Sala de ajedrez José Raúl Capablanca Estado Juan Abrantes Fernández

� <b>JUEVES</b>
�🔫 <b>Tiro Deportivo (M y F)</b> - 9:30 a 15:00H
Profesor Julián Hernández Domínguez 
📞 58452671
🏟️ Campo de tiro del Coppelia

⚽️ <b>Fútbol 11</b> - 14:00 a 17:00H
Profesor Armando Najarro Pérez
📞 5 9745870
🏟️ Terreno de fútbol Estadio universitario Juan Abrantes Fernández 

📅 <b>VIERNES</b>
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

📅 <b>SÁBADOS</b>
🏸 <b>Bádminton (M y F)</b> - 9:00 a 12:00H
(Segundo y cuarto sábado de cada mes)
🏟️ Tabloncillo Ramiro Valdés Daussá 

⚽️ <b>Futsal (M y F)</b> - Concentrado
Profesor José Emilio Cuevas Chávez 
📞 54753187
Profesor Henrry Ordóñez Pedroso 
📞 5 3865784
🏟️ Tabloncillo Ramiro Valdés Daussá"""

    await update.message.reply_text(horarios_texto, parse_mode="HTML")
