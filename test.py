from functions import get_all_emails
from query_function import query_database
import config
import warnings
import pandas as pd

warnings.filterwarnings('ignore')

def retrieve_all_emails(df):
    all_emails = []
    for _, row in df.iterrows():
        imap_host = row['imap_host']
        email = row['email']
        email_password = row['email_password']
        try:
            emails = get_all_emails(imap_host, email, email_password)
            all_emails.extend(emails)
        except Exception as e:
            print("Ocurrió un error en el proceso: ", e)
    return all_emails

if __name__ == "__main__": 
    df = query_database(config.host,
                        config.port,
                        config.user,
                        config.password,
                        config.database,
                        config.schema,
                        config.query)
    
    emails = retrieve_all_emails(df)
    emails_df = pd.DataFrame(emails)
    print(emails_df.head())  # Imprime las primeras 5 filas del DataFrame
