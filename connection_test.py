import pymysql

# CloudType MariaDB 연결 설정
config = {
    'host': 'svc.sel5.cloudtype.app',
    'port': 32134,
    'user': 'root',
    'password': '1111',
    'db': 'mysql',
    'charset': 'utf8mb4'
}

try:
    # 데이터베이스 연결
    conn = pymysql.connect(**config)
    print("CloudType MariaDB 연결 성공!")
    
    # 간단한 테스트 쿼리
    cursor = conn.cursor()
    cursor.execute("SELECT VERSION()")
    version = cursor.fetchone()
    print(f"MariaDB 버전: {version[0]}")
    
    # 데이터베이스 목록 확인
    cursor.execute("SHOW DATABASES")
    databases = cursor.fetchall()
    print(f"데이터베이스 개수: {len(databases)}개")
    
except pymysql.Error as e:
    print(f"연결 실패: {e}")
except Exception as e:
    print(f"오류: {e}")
finally:
    if 'conn' in locals():
        conn.close()
        print("🔐 연결 종료")