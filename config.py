
# Datos de conexión a Postgre
host = "135.125.107.175"
port = "5432"
user = "admin_miguel"
password = "@Neurona12"
database = "milton_project"
schema = 'general_1'

# =============================================================================
# Obtiene datos de suscripciones activas a procesar.
# =============================================================================
query = """
SELECT
  subscriptions.id AS subscription_id,
  subscriptions.start_date,
  subscriptions.end_date,
  agents.agent_name,
  agents.category,
  agent_attributes.context,
  agent_attributes.model,
  hotels.id AS hotel_id,  -- Añadido para recuperar el hotel_id
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
