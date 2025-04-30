# Construir la imagen
echo "Construyendo la imagen 'bot-telegram'..."
docker build -t bot-telegram .

# Ejecutar el contenedor
echo "Ejecutando el contenedor..."
docker run bot-telegram