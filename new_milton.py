from query_function import query_database
import config
from main import get_last_unseen_msg, gpt_model, send_email
import warnings

warnings.filterwarnings('ignore')

def call_milton_for_each_row(df):
    for _, row in df.iterrows():
        context = row['context']
        model = row['model']
        smtp_host = row['smtp_host']
        imap_host = row['imap_host']
        email = row['email']
        email_password = "vjuuntxpciavvfsm"
        
        try:
            re, subject, msg = get_last_unseen_msg(imap_host, email, email_password)
            if re:
                milton_answer = gpt_model(context, msg, model)
                email_sent = send_email(smtp_host, email, email_password, re, subject, milton_answer)
                print(email_sent)
                print(milton_answer)
            else:
                print("Sin emails")
                
        except Exception as e:
            print("Ocurrió un error en el proceso: ", e)

if __name__ == "__main__":
    df = query_database(config.host,
                        config.port,
                        config.user,
                        config.password,
                        config.database,
                        config.schema,
                        config.query)
    call_milton_for_each_row(df)
