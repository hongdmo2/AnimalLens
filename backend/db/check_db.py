import psycopg2
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

def check_database():
    # 연결 정보
    conn_params = {
        'dbname': 'animallens',
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT', '5432')
    }
    
    try:
        # 데이터베이스 연결
        conn = psycopg2.connect(**conn_params)
        cur = conn.cursor()
        
        # 테이블 목록 조회
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cur.fetchall()
        print("\n=== 테이블 목록 ===")
        for table in tables:
            print(table[0])
            
        # animals 테이블 데이터 조회
        print("\n=== Animals 테이블 데이터 ===")
        cur.execute("SELECT * FROM animals")
        animals = cur.fetchall()
        for animal in animals:
            print(f"ID: {animal[0]}")
            print(f"Name: {animal[1]}")
            print(f"Species: {animal[2]}")
            print(f"Habitat: {animal[3]}")
            print(f"Diet: {animal[4]}")
            print(f"Description: {animal[5]}")
            print("---")
            
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    check_database() 