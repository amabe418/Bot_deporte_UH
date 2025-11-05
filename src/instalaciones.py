
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.helpers import escape_markdown
from usuarios import usuario_registrado

instalaciones_info = {}

def cargar_instalaciones():
    global instalaciones_info
    try:
        with open("../BD/instalaciones.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            # Si es una lista (formato antiguo), convertir a diccionario
            if isinstance(data, list):
                instalaciones_info = {inst: {"direccion": "No disponible", "latitud": None, "longitud": None} for inst in data}
            else:
                instalaciones_info = data
    except FileNotFoundError:
        instalaciones_info = {}
        print("[⚠️] Archivo instalaciones.json no encontrado.")


def generar_teclado_instalaciones(pagina: int, elementos_por_pagina: int = 5):
    instalaciones = list(instalaciones_info.keys())
    total_paginas = (len(instalaciones) + elementos_por_pagina - 1) // elementos_por_pagina

    inicio = pagina * elementos_por_pagina
    fin = inicio + elementos_por_pagina
    instalaciones_pagina = instalaciones[inicio:fin]

    # Usar índices en lugar de nombres completos para evitar exceder límite de 64 bytes
    botones = [
        [InlineKeyboardButton(nombre, callback_data=f"instalacion_{inicio + i}")]
        for i, nombre in enumerate(instalaciones_pagina)
    ]

    # Botones de navegación
    botones_navegacion = []
    if pagina > 0:
        botones_navegacion.append(InlineKeyboardButton("⬅️ Anterior", callback_data=f"pagina_instalaciones_{pagina - 1}"))
    if pagina < total_paginas - 1:
        botones_navegacion.append(InlineKeyboardButton("Siguiente ➡️", callback_data=f"pagina_instalaciones_{pagina + 1}"))

    if botones_navegacion:
        botones.append(botones_navegacion)

    return InlineKeyboardMarkup(botones)


@usuario_registrado
async def listar_instalaciones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not instalaciones_info:
        await update.message.reply_text("No hay instalaciones disponibles en este momento.")
        return
    
    reply_markup = generar_teclado_instalaciones(pagina=0)

    await update.message.reply_text(
        "🏟️ Selecciona una instalación para ver más información:",
        reply_markup=reply_markup
    )


@usuario_registrado
async def mostrar_info_instalacion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "volver_instalaciones":
        return await listar_instalaciones_callback(update, context)

    # Obtener el índice del callback_data
    try:
        indice_str = query.data.removeprefix("instalacion_")
        indice = int(indice_str)
        instalaciones_lista = list(instalaciones_info.keys())
        
        if 0 <= indice < len(instalaciones_lista):
            nombre = instalaciones_lista[indice]
        else:
            await query.answer("Error: Instalación no encontrada", show_alert=True)
            return
    except (ValueError, IndexError):
        await query.answer("Error al procesar la solicitud", show_alert=True)
        return
    
    info = instalaciones_info.get(nombre)

    if info:
        direccion = escape_markdown(info.get("direccion", "No disponible"), version=2)
        nombre_escapado = escape_markdown(nombre, version=2)
        latitud = info.get("latitud")
        longitud = info.get("longitud")
        foto_url = info.get("foto", None) or info.get("foto_url", None)

        mensaje = (
            f"🏟️ *{nombre_escapado}*\n\n"
            f"📍 *Dirección:* {direccion}"
        )

        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Volver a la lista", callback_data="volver_instalaciones")]
        ])

        # Si hay foto, enviarla primero con el mensaje como caption
        if foto_url:
            try:
                # Enviar la foto con el mensaje como caption
                await query.message.reply_photo(
                    photo=foto_url,
                    caption=mensaje,
                    reply_markup=reply_markup,
                    parse_mode='MarkdownV2'
                )
                # Editar el mensaje anterior para indicar que hay foto arriba
                try:
                    await query.edit_message_text(
                        text="📷 Foto de la instalación arriba 👆",
                        reply_markup=None
                    )
                except:
                    pass
                
                # Si hay coordenadas, también enviar la ubicación
                if latitud is not None and longitud is not None:
                    try:
                        await query.message.reply_location(
                            latitude=float(latitud),
                            longitude=float(longitud)
                        )
                    except (ValueError, TypeError) as e:
                        print(f"Error al enviar ubicación de la instalación {nombre}: {e}")
            except Exception as e:
                # Si falla enviar la foto, continuar con el flujo normal
                print(f"Error al enviar foto de la instalación {nombre}: {e}")
                foto_url = None  # Continuar sin foto

        # Si no hay foto pero hay ubicación, enviar ubicación y mensaje
        if not foto_url:
            if latitud is not None and longitud is not None:
                try:
                    # Enviar la ubicación en el mapa
                    await query.message.reply_location(
                        latitude=float(latitud),
                        longitude=float(longitud)
                    )
                    # Editar el mensaje anterior con la información
                    await query.edit_message_text(
                        text=mensaje,
                        reply_markup=reply_markup,
                        parse_mode='MarkdownV2'
                    )
                except (ValueError, TypeError) as e:
                    print(f"Error al enviar ubicación de la instalación {nombre}: {e}")
                    await query.edit_message_text(
                        text=mensaje + "\n\n⚠️ No se pudo cargar la ubicación en el mapa.",
                        reply_markup=reply_markup,
                        parse_mode='MarkdownV2'
                    )
            else:
                # Si no hay coordenadas ni foto, mostrar solo el mensaje
                await query.edit_message_text(
                    text=mensaje,
                    reply_markup=reply_markup,
                    parse_mode='MarkdownV2'
                )
    else:
        mensaje = escape_markdown(f"No hay información disponible para {nombre}.", version=2)
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Volver a la lista", callback_data="volver_instalaciones")]
        ])
        await query.edit_message_text(
            text=mensaje,
            reply_markup=reply_markup,
            parse_mode='MarkdownV2'
        )


async def listar_instalaciones_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    pagina = context.user_data.get('pagina_instalaciones', 0)
    
    reply_markup = generar_teclado_instalaciones(pagina=pagina)

    await query.edit_message_text(
        "🏟️ Selecciona una instalación para ver más información:",
        reply_markup=reply_markup
    )


async def cambiar_pagina_instalaciones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Extraer el número de página desde callback_data
    _, _, pagina_str = query.data.split('_')
    pagina = int(pagina_str)

    context.user_data['pagina_instalaciones'] = pagina

    reply_markup = generar_teclado_instalaciones(pagina=pagina)

    await query.edit_message_text(
        text="🏟️ Selecciona una instalación para ver más información:",
        reply_markup=reply_markup
    )


def guardar_instalaciones(data):
    """Guarda las instalaciones en el archivo JSON"""
    global instalaciones_info
    instalaciones_info = data
    with open("../BD/instalaciones.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
