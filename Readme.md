# Bot Deportivo de la Universidad de La Habana

Bot de Telegram diseñado para proporcionar información sobre actividades deportivas, profesores, instalaciones y horarios de entrenamiento de la Universidad de La Habana.

## 🎯 Características Principales

### Para Usuarios
- **Registro de usuarios**: Sistema de registro para estudiantes y profesores
- **Consultar horarios**: Visualización interactiva de horarios por día de la semana
- **Listar deportes**: Información detallada sobre deportes disponibles con profesor, contacto, días, horarios y lugares
- **Listar profesores**: Información completa sobre profesores, incluyendo deportes que imparten, contacto, horarios y fotos
- **Listar instalaciones**: Información sobre instalaciones deportivas con dirección, ubicación en mapa de Telegram y fotos
- **Actividades**: Noticias y actividades próximas relacionadas con los deportes

### Para Administradores
- **Panel de administración**: Acceso completo a funciones de gestión
- **Gestión de deportes**: Agregar, modificar y eliminar deportes
- **Gestión de profesores**: Agregar, modificar y eliminar profesores con soporte para fotos
- **Gestión de instalaciones**: Agregar, modificar y eliminar instalaciones con coordenadas y fotos
- **Subida de fotos**: Sistema para subir fotos directamente al bot (no URLs)

## 📋 Requisitos

- **Python 3.11+**
- **Docker** (opcional, para ejecución con contenedores)
- **Token de Telegram Bot**: Obtenerlo desde [@BotFather](https://t.me/BotFather)

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd Bot_deporte_UH
```

### 2. Configurar el token del bot

Coloca tu token de Telegram en el archivo `token.txt` en la raíz del proyecto:

```bash
echo "TU_TOKEN_AQUI" > token.txt
```

O si prefieres, también puedes colocarlo en `src/token.txt`.

### 3. Instalación de dependencias

#### Opción A: Usando Docker (Recomendado)

```bash
chmod +x docker-run.sh
./docker-run.sh
```

Este script construirá la imagen Docker y ejecutará el contenedor con un volumen persistente para la base de datos.

**⚠️ Importante**: El script monta el directorio `BD/` como volumen, por lo que todos los datos se guardan en tu máquina local y no se pierden al detener el contenedor.

#### Opción B: Instalación local

```bash
cd src
python -m venv ../env
source ../env/bin/activate  # En Windows: ../env\Scripts\activate
pip install -r requirements.txt
```

### 4. Ejecutar el bot

#### Con Docker:
```bash
./docker-run.sh
```

**Nota sobre volúmenes**: El script `docker-run.sh` monta el directorio `BD/` como volumen, asegurando que todos los datos (usuarios, deportes, profesores, instalaciones, administradores) persistan incluso después de detener el contenedor.

#### Localmente:
```bash
cd src
python main.py
```

## 📁 Estructura del Proyecto

```
Bot_deporte_UH/
├── BD/                      # Base de datos (archivos JSON)
│   ├── deportes.json       # Información de deportes
│   ├── profesores.json     # Información de profesores
│   ├── instalaciones.json  # Información de instalaciones
│   ├── usuarios.json       # Usuarios registrados
│   ├── admins.json         # IDs de administradores
│   └── noticias.json       # Noticias y actividades
├── src/                     # Código fuente
│   ├── main.py             # Punto de entrada principal
│   ├── usuarios.py         # Gestión de usuarios y registro
│   ├── deporte.py          # Módulo de deportes
│   ├── profesores.py       # Módulo de profesores
│   ├── instalaciones.py    # Módulo de instalaciones
│   ├── horarios.py         # Gestión de horarios
│   ├── actividades.py      # Noticias y actividades
│   ├── ayuda.py            # Comando de ayuda
│   ├── admin.py            # Gestión de administradores
│   ├── admin_panel.py      # Panel principal de administración
│   ├── admin_deportes.py   # Gestión CRUD de deportes
│   ├── admin_profesores.py # Gestión CRUD de profesores
│   ├── admin_instalaciones.py # Gestión CRUD de instalaciones
│   └── requirements.txt    # Dependencias Python
├── bot.py                  # Versión antigua (no usar)
├── Dockerfile              # Configuración Docker
├── run.sh                  # Script de ejecución Docker
├── token.txt               # Token del bot (no commitear)
└── Readme.md              # Este archivo
```

## 🎮 Comandos Disponibles

### Comandos para Usuarios

- `/start` - Inicia el bot y muestra mensaje de bienvenida
- `/registrar` - Inicia el proceso de registro
- `/horario` - Muestra horarios de entrenamiento por día
- `/listar_deportes` - Lista todos los deportes disponibles
- `/listar_profesores` - Lista todos los profesores disponibles
- `/listar_instalaciones` - Lista todas las instalaciones deportivas
- `/actividades` - Muestra noticias y actividades próximas
- `/ayuda` - Muestra la lista de comandos disponibles

### Funciones de Administrador

Los administradores tienen acceso a un panel especial que se muestra al ejecutar `/start`. Desde allí pueden:

- **Gestión de Deportes**: Agregar, modificar, eliminar y listar deportes
- **Gestión de Profesores**: Agregar, modificar, eliminar y listar profesores (con fotos)
- **Gestión de Instalaciones**: Agregar, modificar, eliminar y listar instalaciones (con coordenadas y fotos)

## 🔐 Sistema de Administración

### Primer Administrador

El primer usuario que se registre en el bot será automáticamente designado como administrador.

### Agregar Administradores

Los administradores se gestionan en el archivo `BD/admins.json`. Para agregar un nuevo administrador:

1. Obtén el `user_id` del usuario en Telegram (puedes usar bots como [@userinfobot](https://t.me/userinfobot))
2. Agrega el ID al array en `BD/admins.json`:

```json
{
  "admins": [
    "123456789",
    "987654321"
  ]
}
```

## 📝 Formato de Datos

### Estructura de Deportes

```json
{
  "Nombre del Deporte": {
    "profesor": "Nombre del profesor",
    "contacto": "Teléfono o email",
    "dias": "Días de práctica",
    "horario": "Horario de práctica",
    "lugar": ["Lugar 1", "Lugar 2"]
  }
}
```

### Estructura de Profesores

```json
{
  "Nombre del Profesor": {
    "deportes": ["Deporte 1", "Deporte 2"],
    "contacto": "Teléfono o email",
    "horarios": "Horarios de clases",
    "lugares": ["Lugar 1", "Lugar 2"],
    "foto": "file_id_de_telegram"
  }
}
```

### Estructura de Instalaciones

```json
{
  "Nombre de la Instalación": {
    "direccion": "Dirección completa",
    "latitud": 23.1363,
    "longitud": -82.3782,
    "foto": "file_id_de_telegram"
  }
}
```

## 📸 Subida de Fotos

Las fotos de profesores e instalaciones deben subirse directamente al bot. El sistema:

1. Detecta automáticamente cuando se envía una foto
2. Guarda el `file_id` de Telegram
3. Las fotos se muestran automáticamente cuando los usuarios consultan la información

**Nota**: No se aceptan URLs, solo fotos enviadas directamente al bot.

## 🗺️ Coordenadas para Instalaciones

Las coordenadas deben estar en formato decimal:
- **Latitud**: Entre -90 y 90
- **Longitud**: Entre -180 y 180
- **Formato**: `latitud,longitud` (ejemplo: `23.1363,-82.3782`)

Puedes obtenerlas desde Google Maps o cualquier aplicación de mapas.

## 🐳 Docker

### Ejecutar con volúmenes (Recomendado)

El script `docker-run.sh` incluye configuración de volúmenes para persistir la base de datos:

```bash
./docker-run.sh
```

Este script:
- Construye la imagen Docker
- Monta el directorio `BD/` como volumen
- Configura el contenedor para reiniciarse automáticamente

### Comandos Docker manuales

#### Construir la imagen manualmente

```bash
docker build -t bot-telegram .
```

**Nota**: El archivo `.dockerignore` está configurado para excluir archivos innecesarios (documentación, entornos virtuales, etc.), haciendo las builds más rápidas y eficientes.

#### Ejecutar el contenedor con volumen

```bash
docker run -d \
    --name bot-telegram-container \
    --restart unless-stopped \
    -v "$(pwd)/BD:/app/BD" \
    -v "$(pwd)/token.txt:/app/token.txt" \
    bot-telegram
```

**Importante**: 
- El flag `-v "$(pwd)/BD:/app/BD"` monta el directorio local `BD/` en el contenedor, asegurando persistencia de datos.
- El flag `-v "$(pwd)/token.txt:/app/token.txt"` monta el archivo de token para que el bot pueda accederlo.

#### Ver logs

```bash
docker logs -f bot-telegram-container
```

#### Detener el contenedor

```bash
docker stop bot-telegram-container
```

#### Eliminar el contenedor

```bash
docker rm bot-telegram-container
```

### Volúmenes y persistencia de datos

El directorio `BD/` y el archivo `token.txt` se montan como volúmenes para que:
- ✅ Los datos persistan después de detener el contenedor
- ✅ Los cambios se reflejen inmediatamente en el sistema de archivos local
- ✅ Puedas hacer backup simplemente copiando el directorio `BD/`
- ✅ Los datos sobrevivan a actualizaciones de la imagen Docker
- ✅ El token se mantenga seguro fuera del contenedor

**Estructura de los volúmenes**:
```
Proyecto/
├── BD/                    # Montado como volumen
│   ├── deportes.json
│   ├── profesores.json
│   ├── instalaciones.json
│   ├── usuarios.json
│   ├── admins.json
│   └── noticias.json
└── token.txt              # Montado como volumen (archivo)
```

### Optimización de builds

El proyecto incluye un archivo `.dockerignore` que excluye:
- Archivos de desarrollo (.git, entornos virtuales, etc.)
- Documentación y archivos README
- Archivos temporales y logs
- Base de datos (se monta como volumen)
- Tokens (se montan como volumen)

Esto hace que las builds de Docker sean más rápidas y eficientes.

## 📚 Documentación Adicional

Para información detallada sobre el uso del bot, consulta el **Manual de Usuario** (disponible en formato LaTeX).

## 🔧 Tecnologías Utilizadas

- **Python 3.11+**
- **python-telegram-bot**: Biblioteca para interactuar con la API de Telegram
- **Docker**: Para contenedorización
- **JSON**: Para almacenamiento de datos

## 📄 Licencia

Este proyecto es propiedad de la Universidad de La Habana.

## 👥 Contribuciones

Para contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama para tu función (`git checkout -b feature/nueva-funcion`)
3. Commit tus cambios (`git commit -am 'Agrega nueva función'`)
4. Push a la rama (`git push origin feature/nueva-funcion`)
5. Abre un Pull Request

## 🐛 Reportar Problemas

Si encuentras algún problema o tienes sugerencias, por favor abre un issue en el repositorio.

## 📞 Soporte

Para soporte técnico o consultas, contacta al equipo de desarrollo.

---

**Desarrollado para la Universidad de La Habana**
