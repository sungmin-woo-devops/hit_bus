import pandas as pd
import pymysql
from pymysql import Error
from typing import Dict, List, Any, Optional
from app.utils.helpers import load_csv_data, get_data_file_path

class Database:
    """team2 전용 데이터베이스 클래스"""
    def __init__(self):
        self.connection = None
        try:
            self.connection = pymysql.connect(
                host='svc.sel5.cloudtype.app',
                port=32134,
                user='root',
                password='1111',
                database='flask_bus',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            print("CloudType MariaDB(flask_bus)에 성공적으로 연결되었습니다.")
        except Error as e:
            print(f"MariaDB 연결 중 오류 발생: {e}")

    def get_data_as_df(self, table_name='suwon_bus_stop_2024'):
        """
        특정 테이블의 데이터를 DataFrame으로 반환합니다.
        Args:
            table_name (str): 조회할 테이블 이름 (기본값: 'suwon_bus_stop_2024')
        Returns:
            pd.DataFrame or None
        """
        if self.connection is None:
            print("데이터베이스 연결이 없습니다.")
            return None
        try:
            with self.connection.cursor() as cursor:
                query = f"SELECT * FROM `{table_name}`;"
                cursor.execute(query)
                result = cursor.fetchall()
                df = pd.DataFrame(result)
                return df
        except Error as e:
            print(f"데이터 조회 중 오류 발생: {e}")
            return None

    def close(self):
        """DB 연결 종료"""
        if self.connection:
            self.connection.close()
            print("MariaDB 연결이 종료되었습니다.")

class DataService:
    """데이터 서비스 클래스"""
    
    def __init__(self):
        self.data_paths = {
            'team2': 'gyeonggi_bus_stop_2023.csv',
            'team3': 'suwon_bus_stop_2024.csv',
            'bus_data': 'bus_data.csv',
            'df_suwon_flask': 'df_suwon_flask.csv'
        }
        # team2 전용 데이터베이스 인스턴스
        self.team2_db = None
    
    def get_team2_db(self):
        """team2 전용 데이터베이스 인스턴스 반환"""
        if self.team2_db is None:
            self.team2_db = Database()
        return self.team2_db
    
    def load_team2_data_from_db(self, table_name='suwon_bus_stop_2024') -> pd.DataFrame:
        """team2 데이터베이스에서 데이터 로드"""
        try:
            db = self.get_team2_db()
            df = db.get_data_as_df(table_name)
            
            if df is not None and not df.empty:
                # 전처리 수행
                df['이용객수'] = pd.to_numeric(df['이용객수'], errors='coerce')

                # DB 스키마에 따라 '시작시간' 컬럼이 없을 수도 있음 → 유연하게 처리
                if '시작시간' not in df.columns:
                    # 만일 '시간' 또는 '시간범위' 컬럼이 있다면 정규식으로 숫자(시)를 추출해 생성
                    time_col = None
                    for col in ['시간', '시간범위', '시작시']:
                        if col in df.columns:
                            time_col = col
                            break
                    if time_col:
                        df['시작시간'] = (
                            df[time_col]
                            .astype(str)
                            .str.extract(r'(\d{1,2})')
                            .astype(float)
                        )
                    else:
                        # 생성 불가 시 NaN 으로 채움
                        df['시작시간'] = pd.NA

                df['시작시간'] = pd.to_numeric(df['시작시간'], errors='coerce')
                df['노선'] = df['노선'].astype(str).str.strip()
            
            if df is not None and not df.empty:
                return df
            # DB 가 비어있으면 CSV 폴백
            print("DB 데이터가 없거나 조회 실패 - CSV로 폴백합니다.")
            return self.load_team2_data()
        except Exception as e:
            print(f"team2 데이터베이스 로드 오류: {e}")
            return pd.DataFrame()
    
    def close_team2_db(self):
        """team2 데이터베이스 연결 종료"""
        if self.team2_db:
            self.team2_db.close()
            self.team2_db = None
    
    def load_team2_data(self) -> pd.DataFrame:
        """Team2 데이터 로드 (기존 CSV 방식)"""
        try:
            file_path = get_data_file_path(self.data_paths['team2'])
            return load_csv_data(file_path)
        except Exception as e:
            print(f"Team2 데이터 로드 오류: {e}")
            return pd.DataFrame()
    
    def load_team3_data(self) -> pd.DataFrame:
        """Team3 데이터 로드"""
        try:
            file_path = get_data_file_path(self.data_paths['team3'])
            return load_csv_data(file_path)
        except Exception as e:
            print(f"Team3 데이터 로드 오류: {e}")
            return pd.DataFrame()
    
    def load_bus_data(self) -> pd.DataFrame:
        """버스 데이터 로드"""
        try:
            file_path = get_data_file_path(self.data_paths['bus_data'])
            return load_csv_data(file_path)
        except Exception as e:
            print(f"버스 데이터 로드 오류: {e}")
            return pd.DataFrame()
    
    def get_available_routes(self, data_type: str = 'team2') -> List[str]:
        """사용 가능한 노선 목록 조회"""
        try:
            if data_type == 'team2':
                # team2는 데이터베이스에서 로드
                df = self.load_team2_data_from_db()
            elif data_type == 'team3':
                df = self.load_team3_data()
            else:
                df = self.load_bus_data()
            
            if df.empty or '노선' not in df.columns:
                return []
            
            return df['노선'].unique().tolist()
        except Exception as e:
            print(f"노선 목록 조회 오류: {e}")
            return []
    
    def get_route_statistics(self, route_name: str, data_type: str = 'team2') -> Dict[str, Any]:
        """특정 노선 통계 조회"""
        try:
            if data_type == 'team2':
                df = self.load_team2_data_from_db()
            elif data_type == 'team3':
                df = self.load_team3_data()
            else:
                df = self.load_bus_data()
            
            if df.empty:
                return {}
            
            # 노선 필터링
            filtered_df = df[df['노선'] == route_name]
            if filtered_df.empty:
                return {}
            
            # 기본 통계
            stats = {
                'route_name': route_name,
                'total_records': len(filtered_df),
                'unique_stops': filtered_df['정류장'].nunique() if '정류장' in filtered_df.columns else 0,
                'total_passengers': filtered_df['이용객수'].sum() if '이용객수' in filtered_df.columns else 0,
                'avg_passengers': filtered_df['이용객수'].mean() if '이용객수' in filtered_df.columns else 0
            }
            
            # 시간대별 통계 (시간 컬럼이 있는 경우)
            if '시간' in filtered_df.columns:
                filtered_df['시작시'] = filtered_df['시간'].str.extract(r'(\d+)').astype(int)
                hourly_stats = filtered_df.groupby('시작시')['이용객수'].agg(['mean', 'sum', 'count']).reset_index()
                stats['hourly_stats'] = hourly_stats.to_dict('records')
            
            # team2 전용 시간대별 통계
            if '시작시간' in filtered_df.columns:
                hourly_stats = filtered_df.groupby('시작시간')['이용객수'].agg(['mean', 'sum', 'count']).reset_index()
                stats['hourly_stats'] = hourly_stats.to_dict('records')
            
            # 월별 통계 (월 컬럼이 있는 경우)
            if '월' in filtered_df.columns:
                monthly_stats = filtered_df.groupby('월')['이용객수'].agg(['mean', 'sum', 'count']).reset_index()
                stats['monthly_stats'] = monthly_stats.to_dict('records')
            
            return stats
            
        except Exception as e:
            print(f"노선 통계 조회 오류: {e}")
            return {}
    
    def get_top_routes(self, data_type: str = 'team2', top_n: int = 5) -> List[Dict[str, Any]]:
        """상위 노선 조회"""
        try:
            if data_type == 'team2':
                df = self.load_team2_data_from_db()
            elif data_type == 'team3':
                df = self.load_team3_data()
            else:
                df = self.load_bus_data()
            
            if df.empty or '노선' not in df.columns:
                return []
            
            # 노선별 통계 계산
            route_stats = df.groupby('노선').agg({
                '이용객수': ['sum', 'mean', 'count']
            }).reset_index()
            
            # 컬럼명 정리
            route_stats.columns = ['노선', '총_이용객수', '평균_이용객수', '기록_수']
            
            # 총 이용객수 기준으로 정렬
            top_routes = route_stats.nlargest(top_n, '총_이용객수')
            
            return top_routes.to_dict('records')
            
        except Exception as e:
            print(f"상위 노선 조회 오류: {e}")
            return []
    
    def get_data_summary(self, data_type: str = 'team2') -> Dict[str, Any]:
        """데이터 요약 정보 조회"""
        try:
            if data_type == 'team2':
                df = self.load_team2_data_from_db()
            elif data_type == 'team3':
                df = self.load_team3_data()
            else:
                df = self.load_bus_data()
            
            if df.empty:
                return {}
            
            summary = {
                'total_records': len(df),
                'total_routes': df['노선'].nunique() if '노선' in df.columns else 0,
                'total_stops': df['정류장'].nunique() if '정류장' in df.columns else 0,
                'total_passengers': df['이용객수'].sum() if '이용객수' in df.columns else 0,
                'avg_passengers': df['이용객수'].mean() if '이용객수' in df.columns else 0,
                'date_range': {
                    'start': df['일시'].min() if '일시' in df.columns else None,
                    'end': df['일시'].max() if '일시' in df.columns else None
                }
            }
            
            return summary
            
        except Exception as e:
            print(f"데이터 요약 조회 오류: {e}")
            return {} 