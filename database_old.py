import pymysql
import pymysql.cursors
import bcrypt
from datetime import datetime
from typing import Optional

class UserDatabase:
    def __init__(self, use_cloud=False, host='localhost', user='root', password='your_password', database='simple_user_db'):
        """
        데이터베이스 연결 초기화
        
        Args:
            use_cloud (bool): True면 CloudType 연결, False면 로컬 연결
            host, user, password, database: 로컬 연결시 사용할 설정
        """
        self.use_cloud = use_cloud
        
        if use_cloud:
            # CloudType MariaDB 연결 설정
            self.host = 'svc.sel5.cloudtype.app'
            self.port = 32134
            self.user = 'root'
            self.password = '1111'
            self.database = 'mysql'
        else:
            # 로컬 데이터베이스 연결 설정
            self.host = host
            self.port = 3306
            self.user = user
            self.password = password
            self.database = database
    
    def get_connection(self):
        """데이터베이스 연결 생성"""
        try:
            if self.use_cloud:
                print(f"CloudType 데이터베이스 연결 중... ({self.host}:{self.port})")
            else:
                print(f"로컬 데이터베이스 연결 중... ({self.host}:{self.port})")
                
            connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            
            if self.use_cloud:
                print("CloudType 연결 성공!")
            else:
                print("로컬 연결 성공!")
                
            return connection
            
        except pymysql.Error as e:
            connection_type = "CloudType" if self.use_cloud else "로컬"
            print(f"{connection_type} 연결 실패: {e}")
            raise
    
    def test_connection(self):
        """연결 테스트"""
        try:
            connection = self.get_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()
                connection_type = "CloudType" if self.use_cloud else "로컬"
                print(f"{connection_type} MariaDB 버전: {version}")
                
                cursor.execute("SHOW DATABASES")
                databases = cursor.fetchall()
                print(f"사용 가능한 데이터베이스: {len(databases)}개")
                
            connection.close()
            return True
        except Exception as e:
            print(f"연결 테스트 실패: {e}")
            return False
    
    def create_user(self, username, email, password, full_name, phone=None, birth_date=None):
        """새 사용자 등록"""
        try:
            # 비밀번호 해시화
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            connection = self.get_connection()
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO test.members (username, email, password_hash, full_name, phone, birth_date)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    username, 
                    email, 
                    password_hash.decode('utf-8'), 
                    full_name, 
                    phone, 
                    birth_date
                ))
                connection.commit()
                return cursor.lastrowid
                
        except pymysql.IntegrityError as e:
            if 'username' in str(e):
                raise ValueError("이미 존재하는 사용자명입니다.")
            elif 'email' in str(e):
                raise ValueError("이미 존재하는 이메일입니다.")
            else:
                raise ValueError("회원가입 중 오류가 발생했습니다.")
        finally:
            connection.close()
    
    def get_all_users(self):
        """모든 사용자 조회 (관리용)"""
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT id, username, email, full_name, phone, birth_date, created_at FROM test.members ORDER BY created_at DESC"
                cursor.execute(sql)
                return cursor.fetchall()
        finally:
            connection.close()
    
    def get_user_by_username(self, username):
        """사용자명으로 사용자 조회"""
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM test.members WHERE username = %s"
                cursor.execute(sql, (username,))
                return cursor.fetchone()
        finally:
            connection.close()

    def authenticate_user(self, username, password):
        """사용자 인증"""
        user = self.get_user_by_username(username)
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            return user
        return None

    def get_user_by_id(self, user_id):
        """ID로 사용자 조회"""
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM test.members WHERE id = %s"
                cursor.execute(sql, (user_id,))
                return cursor.fetchone()
        finally:
            connection.close()


# 편의를 위한 팩토리 함수들
def create_local_db(host='localhost', user='root', password='your_password', database='simple_user_db'):
    """로컬 데이터베이스 인스턴스 생성"""
    return UserDatabase(use_cloud=False, host=host, user=user, password=password, database=database)

def create_cloud_db():
    """CloudType 데이터베이스 인스턴스 생성"""
    return UserDatabase(use_cloud=True)


# 사용 예제
if __name__ == "__main__":
    print("=== 데이터베이스 연결 테스트 ===\n")
    
    # 1. 로컬 데이터베이스 테스트
    print("1. 로컬 데이터베이스:")
    local_db = create_local_db()
    local_db.test_connection()
    
    print("\n" + "="*50 + "\n")
    
    # 2. CloudType 데이터베이스 테스트
    print("2. CloudType 데이터베이스:")
    cloud_db = create_cloud_db()
    cloud_db.test_connection()