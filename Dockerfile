# Utilizar una imagen base oficial de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos del proyecto al directorio de trabajo del contenedor
COPY . /app

# Instalar las dependencias del proyecto
RUN pip install -r requirements.txt

# Exponer el puerto que utiliza tu aplicación
EXPOSE 8105

# Comando para ejecutar la aplicación con Streamlit
CMD streamlit run web.py --server.port 8105 --server.address 0.0.0.0
