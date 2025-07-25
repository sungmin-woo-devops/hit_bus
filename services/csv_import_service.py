import os
import pandas as pd
from sqlalchemy import create_engine, text, inspect
from typing import Optional

# DB 접속 정보 (DB명 없이 접속)
CLOUD_DB_URL_ROOT = 'mysql+pymysql://root:1111@svc.sel5.cloudtype.app:32134/mysql?charset=utf8mb4'
CLOUD_DB_URL = 'mysql+pymysql://root:1111@svc.sel5.cloudtype.app:32134/flask_bus?charset=utf8mb4'

def ensure_database_exists():
    """flask_bus 데이터베이스가 없으면 생성"""
    engine = create_engine(CLOUD_DB_URL_ROOT)
    with engine.connect() as conn:
        conn.execute(text("CREATE DATABASE IF NOT EXISTS flask_bus DEFAULT CHARACTER SET utf8mb4;"))
    print("✅ flask_bus 데이터베이스 확인/생성 완료")

def table_exists(table_name: str) -> bool:
    """테이블 존재 여부 확인"""
    engine = create_engine(CLOUD_DB_URL)
    inspector = inspect(engine)
    return inspector.has_table(table_name)

def import_csv_to_cloud_db(csv_path: str, table_name: Optional[str] = None, if_exists: str = 'replace') -> None:
    """CSV를 flask_bus DB에 테이블로 적재"""
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {csv_path}")
    if table_name is None:
        table_name = os.path.splitext(os.path.basename(csv_path))[0]
    df = pd.read_csv(csv_path)
    print(f"CSV 로드 완료: {csv_path} (행: {len(df)})")
    engine = create_engine(CLOUD_DB_URL)
    df.to_sql(table_name, engine, index=False, if_exists=if_exists, method='multi', chunksize=1000)
    print(f"DB 적재 완료: {table_name} (행: {len(df)})")

def check_table_and_count(table_name: str):
    """테이블 연결 및 행 수 조회"""
    engine = create_engine(CLOUD_DB_URL)
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT COUNT(*) FROM `{table_name}`"))
        count = result.scalar()
    print(f"테이블 `{table_name}`: {count}행")

if __name__ == "__main__":
    # 1. DB 생성
    ensure_database_exists()

    # 2. CSV → 테이블 적재
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    csv_files = [
        'suwon_bus_stop_2024.csv',
        'gyeonggi_bus_stop_2023.csv',
    ]
    for fname in csv_files:
        csv_path = os.path.join(data_dir, fname)
        table = os.path.splitext(fname)[0]
        # 테이블 존재 시 사용자에게 덮어쓰기 여부 확인
        if table_exists(table):
            ans = input(f"테이블 `{table}` 이(가) 이미 존재합니다. 덮어쓰시겠습니까? (y/n): ").strip().lower()
            if ans != 'y':
                print(f"{table} 테이블은 건너뜁니다.")
                continue
            else:
                import_csv_to_cloud_db(csv_path, table, if_exists='replace')
        else:
            import_csv_to_cloud_db(csv_path, table, if_exists='fail')
        check_table_and_count(table)

    print("모든 CSV -> DB 적재 및 연결 확인 완료!")
