# Bot de Deportes de la Universidad de La Habana

Este proyecto es un bot de Telegram diseñado para proporcionar información sobre deporte en la Universidad de La Habana.

## Características

- **Bienvenida**: Mensaje de bienvenida al interactuar con el bot.
- **Lista de deportes**: Información detallada sobre los deportes disponibles, incluyendo el profesor, contacto, días, horarios y lugar.
- **Lista de profesores**: Información sobre el personal docente investigador (PDI).
- **Lista de instalaciones deportivas**: Información sobre las instalaciones deportivas disponibles.
- **Ayuda**: Lista de comandos disponibles.

## Requisitos

- **Docker**

## Instalación y Ejecución

1. **Construcción y ejecución con Docker**:
   - Ejecuta el script `run.sh` para construir la imagen y ejecutar el contenedor:
     ```bash
     ./run.sh
     ```
   - Este script construirá la imagen de Docker con el nombre `bot-telegram` y ejecutará el contenedor.

2. **Interacción con el bot**:
   - Una vez que el contenedor esté en ejecución, puedes interactuar con el bot en Telegram utilizando los comandos disponibles.

## Comandos Disponibles

- `/start`: Mensaje de bienvenida.
- `/horario`: Consultar horarios de entrenamiento (próximamente).
- `/listar_deportes`: Ver la lista de deportes disponibles.
- `/listar_profesores`: Ver la lista de profesores.
- `/listar_instalaciones`: Ver la lista de instalaciones deportivas.
- `/ayuda`: Mostrar la lista de comandos disponibles.