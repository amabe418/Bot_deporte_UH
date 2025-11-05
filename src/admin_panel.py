
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from admin import solo_admins


@solo_admins
async def mostrar_menu_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra el menú principal de administración"""
    
    mensaje = """🔐 <b>PANEL DE ADMINISTRACIÓN</b>

Selecciona una opción para gestionar:"""

    keyboard = [
        [InlineKeyboardButton("🏅 Gestión de Deportes", callback_data="admin_menu_deportes")],
        [InlineKeyboardButton("👨‍🏫 Gestión de Profesores", callback_data="admin_menu_profesores")],
        [InlineKeyboardButton("🏟️ Gestión de Instalaciones", callback_data="admin_menu_instalaciones")],
        [InlineKeyboardButton("🔙 Volver al inicio", callback_data="admin_volver_inicio")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        await update.callback_query.edit_message_text(
            mensaje,
            parse_mode="HTML",
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            mensaje,
            parse_mode="HTML",
            reply_markup=reply_markup
        )


@solo_admins
async def mostrar_submenu_deportes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra el submenú de gestión de deportes"""
    query = update.callback_query
    await query.answer()

    mensaje = """🏅 <b>GESTIÓN DE DEPORTES</b>

Selecciona una acción:"""

    keyboard = [
        [InlineKeyboardButton("➕ Agregar Deporte", callback_data="admin_agregar_deporte")],
        [InlineKeyboardButton("✏️ Modificar Deporte", callback_data="admin_modificar_deporte_lista")],
        [InlineKeyboardButton("🗑️ Eliminar Deporte", callback_data="admin_eliminar_deporte_lista")],
        [InlineKeyboardButton("📋 Listar Deportes", callback_data="admin_listar_deportes")],
        [InlineKeyboardButton("🔙 Volver al menú principal", callback_data="admin_menu_principal")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(mensaje, parse_mode="HTML", reply_markup=reply_markup)


@solo_admins
async def mostrar_submenu_profesores(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra el submenú de gestión de profesores"""
    query = update.callback_query
    await query.answer()

    mensaje = """👨‍🏫 <b>GESTIÓN DE PROFESORES</b>

Selecciona una acción:"""

    keyboard = [
        [InlineKeyboardButton("➕ Agregar Profesor", callback_data="admin_agregar_profesor")],
        [InlineKeyboardButton("✏️ Modificar Profesor", callback_data="admin_modificar_profesor_lista")],
        [InlineKeyboardButton("🗑️ Eliminar Profesor", callback_data="admin_eliminar_profesor_lista")],
        [InlineKeyboardButton("📋 Listar Profesores", callback_data="admin_listar_profesores")],
        [InlineKeyboardButton("🔙 Volver al menú principal", callback_data="admin_menu_principal")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(mensaje, parse_mode="HTML", reply_markup=reply_markup)


@solo_admins
async def mostrar_submenu_instalaciones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra el submenú de gestión de instalaciones"""
    query = update.callback_query
    await query.answer()

    mensaje = """🏟️ <b>GESTIÓN DE INSTALACIONES</b>

Selecciona una acción:"""

    keyboard = [
        [InlineKeyboardButton("➕ Agregar Instalación", callback_data="admin_agregar_instalacion")],
        [InlineKeyboardButton("✏️ Modificar Instalación", callback_data="admin_modificar_instalacion_lista")],
        [InlineKeyboardButton("🗑️ Eliminar Instalación", callback_data="admin_eliminar_instalacion_lista")],
        [InlineKeyboardButton("📋 Listar Instalaciones", callback_data="admin_listar_instalaciones")],
        [InlineKeyboardButton("🔙 Volver al menú principal", callback_data="admin_menu_principal")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(mensaje, parse_mode="HTML", reply_markup=reply_markup)


@solo_admins
async def volver_inicio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Vuelve al mensaje de bienvenida del admin"""
    query = update.callback_query
    await query.answer()
    
    # Limpiar estados de admin
    user_id = str(query.from_user.id)
    if hasattr(context, 'user_data'):
        context.user_data.clear()
    
    # Importar aquí para evitar circular import
    import usuarios
    import admin
    
    user = query.from_user
    user_id = str(user.id)
    
    msg = (
        f"🙌 <b>¡Hola {usuarios.usuarios[user_id]['nombre']}!</b>\n\n"
        "🏟️ Bienvenido de nuevo al Bot de Deportes de la Universidad de La Habana.\n"
        "Explora actividades, entrenamientos y más. 🏀🏐🏊"
    )
    
    teclado = [
        [InlineKeyboardButton("🔐 Panel de Administración", callback_data="admin_menu_principal")],
    ]
    
    await query.edit_message_text(
        msg,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(teclado)
    )

