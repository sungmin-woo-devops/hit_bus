import pandas as pd
import pymysql
from pymysql import Error

class Database:
    def __init__(self):
        self.connection = None
        try:
            self.connection = pymysql.connect(
                host='svc.sel5.cloudtype.app',
                port=32134,
                database='flask_bus',  # 클라우드 DB명으로 변경
                user='root',
                password='1111',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor  # Returns rows as dictionaries
            )
            print("CloudType MariaDB(flask_bus)에 성공적으로 연결되었습니다.")
        except Error as e:
            print(f"MariaDB 연결 중 오류 발생: {e}")

    def get_data_as_df(self, table_name='suwon_bus_stop_2024'):
        """전체 테이블 데이터를 Pandas DataFrame으로 조회"""
        if self.connection is None:
            print("No database connection.")
            return None
        try:
            with self.connection.cursor() as cursor:
                query = f"SELECT * FROM `{table_name}`;"  # 실제 테이블명 사용
                cursor.execute(query)
                result = cursor.fetchall()
                df = pd.DataFrame(result)
                return df
        except Error as e:
            print(f"Error fetching data: {e}")
            return None

    def close(self):
        """DB 연결 종료"""
        if self.connection:
            self.connection.close()
            print("MariaDB 연결이 종료되었습니다.")
