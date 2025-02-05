import psycopg2
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

def run_migration():
    # RDS 연결 정보 (기본 DB)
    conn_params = {
        'dbname': 'postgres',
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT', '5432')
    }
    
    try:
        # PostgreSQL 서버에 연결
        conn = psycopg2.connect(**conn_params)
        conn.autocommit = True
        cur = conn.cursor()
        
        # 1단계: 데이터베이스 생성
        try:
            with open('db/create_db.sql', 'r', encoding='utf-8') as file:
                create_db_sql = file.read()
            cur.execute(create_db_sql)
            print("Database created successfully!")
        except psycopg2.errors.DuplicateDatabase:
            print("Database already exists, continuing...")
        
        # 연결 종료
        cur.close()
        conn.close()
        
        # 2단계: 새 데이터베이스에 연결하여 테이블 생성
        conn_params['dbname'] = 'animallens'
        conn = psycopg2.connect(**conn_params)
        conn.autocommit = True
        cur = conn.cursor()
        
        # 테이블 생성 및 초기 데이터 삽입
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