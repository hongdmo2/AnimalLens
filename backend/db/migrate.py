import psycopg2
import os
from dotenv import load_dotenv
# purpose
# change table schema
# change table relationships

# load .env.development file
load_dotenv('.env.development')


def run_migration():
    # RDS connection information (default DB)
    conn_params = {
        'dbname': os.getenv('DB_NAME', 'animallens'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT', '5432')
    }
    
    try:
        # connect to PostgreSQL server
        conn = psycopg2.connect(**conn_params)
        conn.autocommit = True
        cur = conn.cursor()
        
        # create tables and insert initial data
        with open('db/init_tables.sql', 'r', encoding='utf-8') as file:
            init_tables_sql = file.read()
        cur.execute(init_tables_sql)
        
        print("Tables created and initialized successfully!")
        
    except Exception as e:
        print(f"Error during migration: {e}")
        
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    run_migration() 