"""
통합 데이터 관리자
다양한 데이터 소스(CSV, DB 캐시, 실시간 쿼리)를 지원하는 데이터 관리 클래스
"""
import pandas as pd
import pymysql
import os
import time
from typing import Optional, Dict, Any, List, Union
from threading import Lock
from pymysql import Error
import logging
from contextlib import contextmanager
from dataclasses import dataclass

# 로깅 설정
logger = logging.getLogger(__name__)

@dataclass
class DatabaseConfig:
    """데이터베이스 설정 클래스"""
    host: str = 'svc.sel5.cloudtype.app'
    port: int = 32134
    user: str = 'root'
    password: str = '1234'
    database: str = 'mysql'
    charset: str = 'utf8mb4'
    
    @classmethod
    def from_env(cls) -> 'DatabaseConfig':
        """환경변수에서 설정을 로드"""
        return cls(
            host=os.getenv('DB_HOST', 'svc.sel5.cloudtype.app'),
            port=int(os.getenv('DB_PORT', '32134')),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', '1234'),
            database=os.getenv('DB_NAME', 'mysql'),
            charset=os.getenv('DB_CHARSET', 'utf8mb4')
        )

class DatabaseManager:
    """CloudType MariaDB 연결 관리 클래스"""
    
    def __init__(self, config: Optional[DatabaseConfig] = None):
        """
        DatabaseManager 초기화
        
        Args:
            config: 데이터베이스 설정 (None이면 기본값 사용)
        """
        self.config = config or DatabaseConfig()
        self._connection_params = {
            'host': self.config.host,
            'port': self.config.port,
            'user': self.config.user,
            'password': self.config.password,
            'db': self.config.database,
            'charset': self.config.charset,
            'cursorclass': pymysql.cursors.DictCursor
        }
    
    @contextmanager
    def get_connection(self):
        """
        데이터베이스 연결을 안전하게 관리하는 컨텍스트 매니저
        
        Usage:
            db_manager = DatabaseManager()
            with db_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
        """
        conn: Optional[pymysql.Connection] = None
        try:
            conn = pymysql.connect(**self._connection_params)
            logger.info(f"데이터베이스 연결 성공: {self.config.host}:{self.config.port}")
            yield conn
        except pymysql.Error as e:
            logger.error(f"데이터베이스 연결 오류: {e}")
            raise
        except Exception as e:
            logger.error(f"예상치 못한 오류: {e}")
            raise
        finally:
            if conn:
                conn.close()
                logger.debug("데이터베이스 연결 종료")
    
    def test_connection(self) -> bool:
        """
        데이터베이스 연결 테스트
        
        Returns:
            bool: 연결 성공 시 True, 실패 시 False
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()
                logger.info(f"MariaDB 버전: {version}")
                return True
        except Exception as e:
            logger.error(f"연결 테스트 실패: {e}")
            return False
    
    def execute_query(self, query: str, params: Optional[Union[tuple, list]] = None) -> List[Dict[str, Any]]:
        """
        SELECT 쿼리를 실행하고 결과를 반환
        
        Args:
            query: 실행할 SQL 쿼리
            params: 쿼리 파라미터 (선택사항)
        
        Returns:
            List[Dict]: 쿼리 결과
        
        Usage:
            results = db_manager.execute_query("SELECT * FROM users WHERE id = %s", (1,))
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                results = cursor.fetchall()
                logger.debug(f"쿼리 실행 완료: {len(results)}개 결과")
                return results
        except Exception as e:
            logger.error(f"쿼리 실행 오류: {e}")
            raise
    
    def execute_insert(self, query: str, params: Optional[Union[tuple, list]] = None) -> int:
        """
        INSERT 쿼리를 실행하고 삽입된 행의 ID를 반환
        
        Args:
            query: 실행할 INSERT 쿼리
            params: 쿼리 파라미터 (선택사항)
        
        Returns:
            int: 삽입된 행의 ID (auto_increment)
        
        Usage:
            last_id = db_manager.execute_insert("INSERT INTO users (name) VALUES (%s)", ("홍길동",))
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                last_id = cursor.lastrowid
                logger.debug(f"INSERT 실행 완료: last_id={last_id}")
                return last_id
        except Exception as e:
            logger.error(f"INSERT 실행 오류: {e}")
            raise
    
    def execute_update(self, query: str, params: Optional[Union[tuple, list]] = None) -> int:
        """
        UPDATE/DELETE 쿼리를 실행하고 영향받은 행 수를 반환
        
        Args:
            query: 실행할 UPDATE/DELETE 쿼리
            params: 쿼리 파라미터 (선택사항)
        
        Returns:
            int: 영향받은 행 수
        
        Usage:
            affected_rows = db_manager.execute_update("UPDATE users SET name = %s WHERE id = %s", ("김철수", 1))
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                affected_rows = cursor.execute(query, params)
                conn.commit()
                logger.debug(f"UPDATE/DELETE 실행 완료: {affected_rows}개 행 영향")
                return affected_rows
        except Exception as e:
            logger.error(f"UPDATE/DELETE 실행 오류: {e}")
            raise
    
    def execute_many(self, query: str, params_list: List[Union[tuple, list]]) -> int:
        """
        여러 행을 한 번에 실행 (배치 처리)
        
        Args:
            query: 실행할 SQL 쿼리
            params_list: 파라미터 리스트
        
        Returns:
            int: 영향받은 총 행 수
        
        Usage:
            data = [("홍길동", 25), ("김철수", 30)]
            rows = db_manager.execute_many("INSERT INTO users (name, age) VALUES (%s, %s)", data)
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                affected_rows = cursor.executemany(query, params_list)
                conn.commit()
                logger.debug(f"배치 실행 완료: {affected_rows}개 행 영향")
                return affected_rows
        except Exception as e:
            logger.error(f"배치 실행 오류: {e}")
            raise
    
    def get_table_info(self, table_name: str) -> List[Dict[str, Any]]:
        """
        테이블 구조 정보를 반환
        
        Args:
            table_name: 테이블 이름
        
        Returns:
            List[Dict]: 테이블 컬럼 정보
        """
        return self.execute_query(f"DESCRIBE {table_name}")
    
    def get_databases(self) -> List[str]:
        """
        사용 가능한 데이터베이스 목록을 반환
        
        Returns:
            List[str]: 데이터베이스 이름 목록
        """
        results = self.execute_query("SHOW DATABASES")
        return [db['Database'] for db in results]
    
    def get_tables(self) -> List[str]:
        """
        현재 데이터베이스의 테이블 목록을 반환
        
        Returns:
            List[str]: 테이블 이름 목록
        """
        results = self.execute_query("SHOW TABLES")
        key = f"Tables_in_{self.config.database}"
        return [table[key] for table in results]

# 전역 데이터베이스 매니저 인스턴스 (싱글톤 패턴)
db_manager = DatabaseManager()

# 편의 함수들
def get_db_connection():
    """전역 데이터베이스 매니저의 연결을 반환"""
    return db_manager.get_connection()

def execute_query(query: str, params: Optional[Union[tuple, list]] = None) -> List[Dict[str, Any]]:
    """전역 데이터베이스 매니저로 쿼리 실행"""
    return db_manager.execute_query(query, params)

def execute_insert(query: str, params: Optional[Union[tuple, list]] = None) -> int:
    """전역 데이터베이스 매니저로 INSERT 실행"""
    return db_manager.execute_insert(query, params)

def execute_update(query: str, params: Optional[Union[tuple, list]] = None) -> int:
    """전역 데이터베이스 매니저로 UPDATE/DELETE 실행"""
    return db_manager.execute_update(query, params) 