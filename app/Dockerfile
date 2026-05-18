# Imagen base del proyecto
FROM python:3.11-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos las dependencias del proyecto
COPY requirements.txt .

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del codigo
COPY . .

# Puerto por donde corre Flask
EXPOSE 5000

# Comando que se ejecuta cuando arranca el contenedor
CMD ["python", "app.py"]
