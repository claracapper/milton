import functions as f
from query_function import query_database
import config
import warnings
import pandas as pd
import psycopg2

warnings.filterwarnings('ignore')

def save_email_to_database(host, port, user, password, database, schema, email):
    conn = None
    try:
        # Conecta a la base de datos PostgreSQL
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )

        # Crea un nuevo cursor
        cur = conn.cursor()

        # Inserta el email en la base de datos
        cur.execute(f"""
            INSERT INTO {schema}.emails (email_from, subject, email_body)
            VALUES (%s, %s, %s)
        """, (email['email_from'], email['email_subject'], email['email_body']))

        # Commit the transaction
        conn.commit()

        # Cierra la comunicación con la base de datos
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def retrieve_all_emails(df):
    all_emails = []
    for _, row in df.iterrows():
        imap_host = row['imap_host']
        email = row['email']
        email_password = row['email_password']
        try:
            email = f.get_last_unseen_msg(imap_host, email, email_password)
            if email['email_from'] is not None:
                all_emails.append(email)
                save_email_to_database(config.host,
                                       config.port,
                                       config.user,
                                       config.password,
                                       config.database,
                                       config.schema,
                                       email)
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