
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
query = """SELECT
  subscriptions.id AS subscription_id,
  subscriptions.start_date,
  subscriptions.end_date,
  products.agent_name,
  products.category,
  product_attributes.context,
  product_attributes.model,
  hotels.smtp_host,
  hotels.imap_host,
  hotels.email,
  hotels.email_password
FROM
  subscriptions
INNER JOIN products ON subscriptions.agent_id = products.id
INNER JOIN product_attributes ON products.id = product_attributes.agent_id
INNER JOIN hotels ON subscriptions.hotels_ids = hotels.id
WHERE
  subscriptions.is_active = TRUE
  AND subscriptions.end_date > CURRENT_DATE;
"""