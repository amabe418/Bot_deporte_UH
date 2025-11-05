# Imagen base de Python
FROM python:3.11-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . .

# Cambia al directorio src y instala las dependencias
WORKDIR /app/src

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Declara el volumen para la base de datos
# Esto permite que los datos persistan fuera del contenedor
VOLUME ["/app/BD"]

# Comando para ejecutar el bot (desde src/)
CMD ["python", "main.py"]
