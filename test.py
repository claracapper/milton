import functions as f
from query_function import query_database
import config
import warnings
import pandas as pd

warnings.filterwarnings('ignore')

if __name__ == "__main__": 
    df = query_database(config.host,
                        config.port,
                        config.user,
                        config.password,
                        config.database,
                        config.schema,
                        config.query)

    emails = f.process_email(df)
    emails_df = pd.DataFrame(emails)
    
    f.process_and_respond_emails()