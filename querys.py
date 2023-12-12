# =============================================================================
# CUSTOMERS
# =============================================================================
# Crea nuevo cliente
query0 = "INSERT INTO customers (customer_name, is_active) VALUES ('Nombre del Cliente', TRUE);"

# Lee todos los clientes
query1 = "SELECT * FROM customers;"

# Lee un cliente específico por ID
query2 = "SELECT * FROM customers WHERE id = 1;"

# Actualiza un cliente
query3 = "UPDATE customers SET customer_name = 'Nuevo Nombre' WHERE id = 1;"

# Actualiza un cliente
query4 = "DELETE FROM customers WHERE id = 1;"
# =============================================================================
# HOTELS
# =============================================================================
# Crea nuevo hotel
query5 = "INSERT INTO hotels (hotel_name, customer_id, address, email, is_active) VALUES ('Nombre del Hotel', 1, 'Dirección del Hotel', 'email@hotel.com', TRUE);"

# Lee todos los hoteles
query6 = "SELECT * FROM hotels;"

# Lee hoteles de un cliente específico
query7 = "SELECT * FROM hotels WHERE customer_id = 1;"

# Actualiza un hotel específico
query8 = "UPDATE hotels SET hotel_name = 'Nuevo Nombre del Hotel' WHERE id = 1;"

# Elimina un hotel
query9 = "DELETE FROM hotels WHERE id = 1;"
# =============================================================================
# PRODUCTS
# =============================================================================
# Lee todos los productos
query10 = "SELECT * FROM products;"

# Actualiza un producto 
query11 = "UPDATE products SET category = 'Nueva Categoría' WHERE id = 1;"

# Elimina un producto
query12 = "DELETE FROM products WHERE id = 1;"
# =============================================================================
# PRODUCT ATTRIBUTES
# =============================================================================
# Crear un nuevo atributo de producto
query12 = "INSERT INTO product_attributes (agent_id, customer_id, hotels_id, context, model, is_active) VALUES (1, 1, 1, 'Contexto', 'Modelo', TRUE);"

# Leer atributos de productos
query13 = "SELECT * FROM product_attributes WHERE agent_id = 1;"

# Actualizar atributos de un producto
query14 = "UPDATE product_attributes SET context = 'Nuevo Contexto' WHERE id = 1;"

# Eliminar atributos de un producto
query15 = "DELETE FROM product_attributes WHERE id = 1;"
# =============================================================================
# SUBSCRIPTIONS
# =============================================================================
# Crear una nueva suscripción
query16 = "INSERT INTO subscriptions (agent_id, start_date, end_date, customer_id, hotels_ids, is_active) VALUES (1, CURRENT_DATE, CURRENT_DATE + INTERVAL '1 year', 1, 1, TRUE);"

# Leer suscripciones
query17 = "SELECT * FROM subscriptions WHERE customer_id = 1;"

# Actualizar una suscripción
query18 = "UPDATE subscriptions SET end_date = CURRENT_DATE + INTERVAL '2 years' WHERE id = 1;"

# Eliminar una suscripción
query19 = "DELETE FROM subscriptions WHERE id = 1;"
# =============================================================================
# SCHEDULES
# =============================================================================
# Crear un nuevo horario
query20 = "INSERT INTO schedules (last_activation_time, customer_id, hotels_id, is_active) VALUES (CURRENT_TIMESTAMP, 1, 1, TRUE);"

# Leer horarios
query21 = "SELECT * FROM schedules WHERE customer_id = 1;"

# Actualizar un horario
query22 = "UPDATE schedules SET last_activation_time = CURRENT_TIMESTAMP WHERE id = 1;"

# Eliminar un horario
query23 = "DELETE FROM schedules WHERE id = 1;"

