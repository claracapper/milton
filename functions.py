import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import decode_header
import re
from openai import OpenAI
import datetime
import config
import psycopg2
import pandas as pd
import pytz
from email.utils import parsedate_tz, mktime_tz

# =============================================================================
# OBTENCIÓN ÚLTIMO EMAIL SIN ABRIR
# =============================================================================
def get_last_unseen_msg(imap_host, username, password):
    def decode_msg(msg):
        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                cdispo = str(part.get('Content-Disposition'))

                if ctype == 'text/plain' and 'attachment' not in cdispo:
                    return part.get_payload(decode=True).decode('utf-8')
        else:
            return msg.get_payload(decode=True).decode('utf-8')

    try:
        mail = imaplib.IMAP4_SSL(imap_host)
        mail.login(username, password)
        mail.select('inbox')

        status, messages = mail.search(None, 'UNSEEN')
        if status == "OK" and messages[0]:
            num = messages[0].split()[-1]  # Obtener el último correo no leído
            status, data = mail.fetch(num, '(RFC822)')
            if status == 'OK':
                msg = email.message_from_bytes(data[0][1])
                remitente_completo = msg['From']
                asunto = msg['Subject']
                mensaje = decode_msg(msg)
                msg_id = msg['Message-ID']  # Obtener el ID del mensaje
                fecha_recibido = msg['Date']  # Obtener la fecha de recepción del mensaje

                # Ajustar la zona horaria
                tz = pytz.timezone('Europe/Madrid')
                date_tuple = parsedate_tz(fecha_recibido)
                if date_tuple:
                    local_date = datetime.datetime.fromtimestamp(mktime_tz(date_tuple), tz)

                # Extraer la dirección de correo electrónico del remitente
                remitente = re.search(r'<(.+?)>', remitente_completo)
                remitente_email = remitente.group(1) if remitente else remitente_completo

                # Decodificar el asunto si es necesario
                if asunto is not None:
                    asunto_decodificado, encoding = decode_header(asunto)[0]
                    if isinstance(asunto_decodificado, bytes):
                        asunto = asunto_decodificado.decode(encoding or 'utf-8')
                else:
                    asunto = " "

                return {
                    'email_from': remitente_email,
                    'email_subject': asunto,
                    'email_body': mensaje,
                    'msg_id': msg_id,
                    'received_date': local_date.strftime("%Y-%m-%d %H:%M:%S")
                }

        return {
            'email_from': None,
            'email_subject': None,
            'email_body': None,
            'msg_id': None,
            'received_date': None
        }
    except Exception as e:
        print("Ocurrió un error:", e)
        return {
            'email_from': None,
            'email_subject': None,
            'email_body': None,
            'msg_id': None,
            'received_date': None
        }

# =============================================================================
# 
# =============================================================================
def process_email(df):
    all_emails = []
    for _, row in df.iterrows():
        imap_host = row['imap_host']
        email = row['email']
        email_password = row['email_password']
        hotel_id = row['hotel_id']
        try:
            email = get_last_unseen_msg(imap_host, email, email_password)
            if email['email_from'] is not None:
                all_emails.append(email)
                save_email_to_database(config.host,
                                       config.port,
                                       config.user,
                                       config.password,
                                       config.database,
                                       config.schema,
                                       email,
                                       hotel_id)
        except Exception as e:
            print("Ocurrió un error en el proceso: ", e)
    return all_emails
# =============================================================================
# 
# =============================================================================
def gpt_model(contexto,
            mensaje,
            model,
            temperature=0):
    
    now = datetime.datetime.now()
    fecha = now.strftime("%d de %B de %Y")
    hora = now.strftime("%H:%M")

    fecha_hora = f"Hoy es {fecha}, son las {hora}h"
    datetime_info = f"Esta es la hora que tienes en cuenta al saludar, buenos días de 7AM a 12PM, buenas tardes de 12PM a 20PM y buenas noches de 21PM a 7AM: {fecha_hora}"
    idioma = "recuerda responder en el mismo idioma que el mensaje del cliente, que es el siguiente:"
    
    client = OpenAI(api_key="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")  

    context =  contexto + datetime_info  + idioma + mensaje
    response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": context}],
            temperature=temperature,
            #max_tokens=100
        )
    
    respuesta = response.choices[0].message.content

    return respuesta
# =============================================================================
# 
# =============================================================================
def send_email(smtp_host, username, password, remitente, asunto, respuesta, msg_id):
    # Crear el mensaje
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = remitente
    msg['Subject'] = 'Re: ' + asunto
    msg['In-Reply-To'] = msg_id  # Añadir el ID del mensaje al que se está respondiendo
    msg.attach(MIMEText(respuesta, 'plain'))

    try:
        # Conectar al servidor SMTP y enviar el correo
        server = smtplib.SMTP(smtp_host, 587)
        server.starttls()
        server.login(username, password)
        server.send_message(msg)
        server.quit()
        return "Correo enviado exitosamente a {}".format(remitente)
    except Exception as e:
        return "Error al enviar correo: {}".format(str(e))
    
# =============================================================================
# 
# =============================================================================

def get_all_emails(imap_host, username, password):
    def decode_msg(msg):
        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                cdispo = str(part.get('Content-Disposition'))
    
                if ctype == 'text/plain' and 'attachment' not in cdispo:
                    try:
                        return part.get_payload(decode=True).decode('utf-8')
                    except UnicodeDecodeError:
                        return part.get_payload(decode=True).decode('utf-8', 'replace')
        else:
            try:
                return msg.get_payload(decode=True).decode('utf-8')
            except UnicodeDecodeError:
                return msg.get_payload(decode=True).decode('utf-8', 'replace')
    try:
        mail = imaplib.IMAP4_SSL(imap_host)
        mail.login(username, password)
        mail.select('inbox')

        status, messages = mail.search(None, 'ALL')  # Cambiado de 'UNSEEN' a 'ALL'
        if status == "OK":
            all_emails = []
            for num in messages[0].split():  # Iterar sobre todos los correos
                status, data = mail.fetch(num, '(RFC822)')
                if status == 'OK':
                    msg = email.message_from_bytes(data[0][1])
                    remitente_completo = msg['From']
                    asunto = msg['Subject']
                    mensaje = decode_msg(msg)
                    msg_id = msg['Message-ID']

                    remitente = re.search(r'<(.+?)>', remitente_completo)
                    remitente_email = remitente.group(1) if remitente else remitente_completo

                    if asunto is not None:
                        asunto_decodificado, encoding = decode_header(asunto)[0]
                        if isinstance(asunto_decodificado, bytes):
                            asunto = asunto_decodificado.decode(encoding or 'utf-8')
                    else:
                        asunto = " "

                    # Añadir el correo electrónico a la lista
                    all_emails.append({
                        'email_from': remitente_email,
                        'email_subject': asunto,
                        'email_body': mensaje,
                        'email_id': msg_id
                    })
            return all_emails
    except Exception as e:
        print("Ocurrió un error:", e)
        return []

# =============================================================================
# 
# =============================================================================
def save_email_to_database(host, port, user, password, database, schema, email, hotel_id):
    conn = None
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        cur = conn.cursor()
        received_date = pd.to_datetime(email['received_date'], utc=True).strftime('%Y-%m-%d %H:%M:%S')

        # Modificar la consulta SQL para incluir el campo received_date
        cur.execute(f"""
            INSERT INTO {schema}.emails (email_from, subject, email_body, received_date, hotel_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (email['email_from'], email['email_subject'], email['email_body'], received_date, hotel_id))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

# =============================================================================
# 
# =============================================================================
def respond_and_save_emails():
    conn = None
    try:
        # Conexión a la base de datos
        conn = psycopg2.connect(
            host=config.host,
            port=config.port,
            user=config.user,
            password=config.password,
            database=config.database
        )
        cur = conn.cursor()

        # Leer emails sin respuesta generada
        cur.execute("""
            SELECT id, email_body, hotel_id, received_date FROM general_1.emails
            WHERE generated_response IS NULL
        """)
        emails = cur.fetchall()

        for email_id, email_body, hotel_id, received_date in emails:
            # Buscar información del hotel
            cur.execute("""
                SELECT context, model FROM general_1.agent_attributes
                WHERE hotel_id = %s
            """, (hotel_id,))
            agent_info = cur.fetchone()
            if agent_info:
                context, model = agent_info

                # Generar respuesta con el modelo GPT
                generated_response = gpt_model(context, email_body, model)

                # Obtener el timestamp actual y convertirlo a la zona horaria local
                current_time = datetime.datetime.now(pytz.utc)
                local_tz = pytz.timezone('Europe/Madrid')
                local_time = current_time.astimezone(local_tz)

                # Guardar la respuesta generada y el timestamp en la base de datos
                cur.execute("""
                    UPDATE general_1.emails
                    SET generated_response = %s, answered_date = %s
                    WHERE id = %s
                """, (generated_response, local_time, email_id))
                conn.commit()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error al procesar y responder emails:", error)
    finally:
        if conn is not None:
            conn.close()
            
# =============================================================================
# 
# =============================================================================
def get_hotel_name(config, hotel_id):
    """
    Obtiene el nombre del hotel basado en su ID utilizando la configuración de la base de datos.

    Parámetros:
    - config: Un diccionario con la configuración de la base de datos.
    - hotel_id: El ID del hotel.

    Retorna:
    - El nombre del hotel si se encuentra, o None si no se encuentra.
    """
    conn = None
    try:
        conn = psycopg2.connect(
            host=config["host"],
            port=config["port"],
            user=config["user"],
            password=config["password"],
            dbname=config["database"]
        )
        cur = conn.cursor()
        cur.execute("""
            SELECT hotel_name FROM general_1.hotels
            WHERE id = %s
        """, (hotel_id,))
        result = cur.fetchone()
        if result:
            return result[0]
        return None
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error al obtener el nombre del hotel: {error}")
        return None
    finally:
        if conn is not None:
            conn.close()