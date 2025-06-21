
PROJECT_DIR="./src"

if [ ! -d "$PROJECT_DIR" ]; then
  echo "❌ Error: La carpeta 'src' no existe en el directorio actual."
  exit 1
fi

cd "$PROJECT_DIR" || exit 1


echo "Instalando dependencias..."
python -m pip install -r requirements.txt  


echo "Iniciando el bot de Telegram..."
python main.py  