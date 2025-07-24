import pymysql
import pymysql.cursors
import bcrypt
from datetime import datetime

class UserDatabase:
    def __init__(self, host='localhost', user='root', password='your_password', database='simple_user_db'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
    
    def get_connection(self):
        """데이터베이스 연결 생성"""
        return pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    
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