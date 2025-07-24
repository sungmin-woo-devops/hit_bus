import pandas as pd
import pymysql
from pymysql import Error

class Database:
    def __init__(self):
        self.connection = None
        try:
            self.connection = pymysql.connect(
                host='localhost',
                port=3306,
                user='root',
                password='0000',  # 실제 비밀번호
                database='suwondb',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor  # 결과를 딕셔너리로 반환
            )
            print("✅ MariaDB에 성공적으로 연결되었습니다.")
        except Error as e:
            print(f"❌ MariaDB 연결 중 오류 발생: {e}")

    def get_data_as_df(self, table_name='suwon'):
        """
        특정 테이블의 데이터를 DataFrame으로 반환합니다.
        Args:
            table_name (str): 조회할 테이블 이름 (기본값: 'suwon')
        Returns:
            pd.DataFrame or None
        """
        if self.connection is None:
            print("❌ 데이터베이스 연결이 없습니다.")
            return None
        try:
            with self.connection.cursor() as cursor:
                query = f"SELECT * FROM {table_name};"
                cursor.execute(query)
                result = cursor.fetchall()
                df = pd.DataFrame(result)
                return df
        except Error as e:
            print(f"❌ 데이터 조회 중 오류 발생: {e}")
            return None

    def close(self):
        """DB 연결 종료"""
        if self.connection:
            self.connection.close()
            print("🔌 MariaDB 연결이 종료되었습니다.")
