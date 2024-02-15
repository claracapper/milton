import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import decode_header
import re
from openai import OpenAI
# =============================================================================
# OBTENCIÓN ÚLTIMO EMAIL SIN ABRIR
# =============================================================================

def get_last_unseen_msg(imap_host, username, password):
    def decodificar_mensaje(msg):
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
        if status == "OK":
            if messages[0]:
                num = messages[0].split()[-1]  # Obtener el último correo no leído
                status, data = mail.fetch(num, '(RFC822)')
                if status == 'OK':
                    msg = email.message_from_bytes(data[0][1])
                    remitente_completo = msg['From']
                    asunto = msg['Subject']
                    mensaje = decodificar_mensaje(msg)

                    # Extraer la dirección de correo electrónico del remitente
                    remitente = re.search(r'<(.+?)>', remitente_completo)
                    remitente_email = remitente.group(1) if remitente else remitente_completo

                    # Decodificar el asunto si es necesario
                    asunto_decodificado, encoding = decode_header(asunto)[0]
                    if isinstance(asunto_decodificado, bytes):
                        asunto = asunto_decodificado.decode(encoding or 'utf-8')

                    return remitente_email, asunto, mensaje
            return None, None, None
    except Exception as e:
        print("Ocurrió un error:", e)
        return None, None, None

# =============================================================================
# 
# =============================================================================

def gpt_request(contexto,
            mensaje,
            model,
            temperature=0):

    client = OpenAI(api_key="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")  
    context = contexto  + mensaje  
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
def send_email(smtp_host, username, password, remitente, asunto, respuesta):
    # Crear el mensaje
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = remitente
    msg['Subject'] = 'Re: ' + asunto
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

