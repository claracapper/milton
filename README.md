# Propósito de cada Script

config.toml
Propósito: Almacenar las configuraciones esenciales para la conexión a la base de datos y otros parámetros de configuración del entorno. Facilita la gestión de variables de entorno de forma segura y centralizada.

demo_feb.py
Propósito: Demostrar el uso del modelo GPT-3 para generar respuestas automáticas basadas en un contexto predefinido. Este script incluye una simulación de escritura en tiempo real para mostrar cómo se podría integrar la respuesta del modelo en aplicaciones interactivas.

functions.py
Propósito: Proporcionar funciones de utilidad que son usadas por otros scripts del proyecto, especialmente para interactuar con el modelo GPT-3 y procesar las respuestas generadas.

main.py
Propósito: Actuar como el punto de entrada principal del proyecto, integrando las diferentes funciones y módulos para ejecutar la lógica de negocio central. Coordina las operaciones entre la base de datos y la API de GPT-3.

query_function.py
Propósito: Ofrecer funciones especializadas para ejecutar consultas SQL, simplificando la interacción con la base de datos mediante la abstracción de la conexión y ejecución de consultas.

querys.py
Propósito: Definir un conjunto de consultas SQL preconfiguradas que se utilizan a lo largo del proyecto para realizar operaciones CRUD (crear, leer, actualizar, eliminar) en la base de datos.

bbdd_module.py
Propósito: Manejar todas las operaciones relacionadas con la base de datos, incluyendo la conexión, ejecución de consultas y cierre de conexiones. Proporciona una interfaz consistente para la recuperación y manipulación de datos en forma de DataFrames.

