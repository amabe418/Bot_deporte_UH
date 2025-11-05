#!/bin/bash

# Script para ejecutar el bot con Docker usando volúmenes

IMAGE_NAME="bot-telegram"
CONTAINER_NAME="bot-telegram-container"

# Verificar si el contenedor ya existe
if docker ps -a | grep -q "$CONTAINER_NAME"; then
    echo "🛑 Deteniendo y eliminando contenedor existente..."
    docker stop "$CONTAINER_NAME" > /dev/null 2>&1
    docker rm "$CONTAINER_NAME" > /dev/null 2>&1
fi

# Construir la imagen si no existe o forzar reconstrucción
echo "🔨 Construyendo imagen Docker..."
docker build -t "$IMAGE_NAME" .

# Verificar que el token existe
if [ ! -f "./token.txt" ]; then
    echo "❌ Error: token.txt no encontrado en el directorio raíz"
    echo "   Por favor, crea el archivo token.txt con tu token de Telegram Bot"
    exit 1
fi

# Verificar que el directorio BD existe
if [ ! -d "./BD" ]; then
    echo "⚠️  Creando directorio BD..."
    mkdir -p ./BD
fi

# Ejecutar el contenedor con volumen para BD y token
echo "🚀 Iniciando contenedor con volúmenes para BD y token..."
docker run -d \
    --name "$CONTAINER_NAME" \
    --restart unless-stopped \
    -v "$(pwd)/BD:/app/BD" \
    -v "$(pwd)/token.txt:/app/token.txt" \
    "$IMAGE_NAME"

if [ $? -eq 0 ]; then
    echo "✅ Bot iniciado correctamente!"
    echo "📊 Ver logs con: docker logs -f $CONTAINER_NAME"
    echo "🛑 Detener con: docker stop $CONTAINER_NAME"
    echo "📁 Los datos se guardan en: $(pwd)/BD"
else
    echo "❌ Error al iniciar el contenedor"
    exit 1
fi

