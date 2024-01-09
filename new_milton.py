from query_function import query_database
import config
from main import get_last_unseen_msg, gpt_model, send_email
import warnings
import time

warnings.filterwarnings('ignore')

df = query_database(config.host,
                    config.port,
                    config.user,
                    config.password,
                    config.database,
                    config.schema,
                    config.query)

# =============================================================================
# 
# =============================================================================
def call_milton_for_each_row(df):
    for _, row in df.iterrows():
        # Se obtienen los datos del hotel.
        context=row['context']
        model=row['model']
        smtp_host=row['smtp_host']
        imap_host=row['imap_host']
        email=row['email']
        email_password=row['email_password']
        
        try:
            # Obtiene último mail leído
            re, subject, msg = get_last_unseen_msg(imap_host, email, email_password)
            
            if re:
                # Milton
                milton_answer = gpt_model(context, msg, model)
                
                # Envío de mensaje
                email_sent = send_email(smtp_host, email, email_password, re, subject, milton_answer)
                
                print(email_sent)
                print(milton_answer)
            else:
                print("Sin emails")
                
        except Exception as e:
            print("Ocurrió un error en el proceso: ", e)

while True:
    call_milton_for_each_row(df)
    time.sleep(30) 


        
        


