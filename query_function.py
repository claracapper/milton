import psycopg2
import pandas as pd

def query_database(host, port, user, password, database, schema, query):
    # Establecer conexión
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        # Configurar el esquema de búsqueda
        cursor = conn.cursor()
        cursor.execute(f"SET search_path TO {schema}")
        cursor.close()
        print("Conexión exitosa a la base de datos.")
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

    # Inicializar df para asegurar que está definido
    df = pd.DataFrame()
    try:
        # Ejecutar la consulta y obtener los resultados en un DataFrame
        df = pd.read_sql_query(query, conn)
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
    finally:
        # Cerrar conexión
        conn.close()

    return df

query = """SELECT
  subscriptions.id AS subscription_id,
  subscriptions.start_date,
  subscriptions.end_date,
  agents.agent_name,
  agents.category,
  agent_attributes.context,
  agent_attributes.model,
  hotels.smtp_host,
  hotels.imap_host,
  hotels.email,
  hotels.email_password
FROM
  subscriptions
INNER JOIN agents ON subscriptions.agent_id = agents.id
INNER JOIN agent_attributes ON agents.id = agent_attributes.agent_id
INNER JOIN hotels ON subscriptions.hotels_ids = hotels.id
WHERE
  subscriptions.is_active = TRUE
  AND subscriptions.end_date > CURRENT_DATE;
"""

