import os
import json
import pandas as pd
from typing import Dict, List, Any, Optional
from flask import current_app

def load_csv_data(file_path: str) -> pd.DataFrame:
    """CSV 파일 로드"""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"CSV 파일 로드 오류: {e}")
        return pd.DataFrame()

def load_json_data(file_path: str) -> Dict[str, Any]:
    """JSON 파일 로드"""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"JSON 파일 로드 오류: {e}")
        return {}

def get_data_file_path(filename: str) -> str:
    """데이터 파일 경로 생성"""
    if current_app:
        return os.path.join(current_app.root_path, '..', 'data', filename)
    else:
        return os.path.join(os.path.dirname(__file__), '..', '..', 'data', filename)

def get_static_file_path(filename: str) -> str:
    """정적 파일 경로 생성"""
    if current_app:
        return os.path.join(current_app.root_path, '..', 'static', filename)
    else:
        return os.path.join(os.path.dirname(__file__), '..', '..', 'static', filename)

def format_bus_data(df: pd.DataFrame, route_column: str = '노선') -> List[Dict[str, Any]]:
    """버스 데이터 포맷팅"""
    try:
        # 상위 노선 추출
        top_routes = df[route_column].value_counts().head(4).index.tolist()
        
        # 시간대별 평균 이용객수 계산
        if '시간' in df.columns and '이용객수' in df.columns:
            df['시작시'] = df['시간'].str.extract(r'(\d+)').astype(int)
            grouped = df.groupby('시작시')['이용객수'].mean().sort_index()
            chart_labels = list(grouped.index)
            chart_values = list(grouped.values)
        else:
            chart_labels = []
            chart_values = []
        
        return {
            'top_routes': top_routes,
            'chart_labels': chart_labels,
            'chart_values': chart_values
        }
    except Exception as e:
        print(f"버스 데이터 포맷팅 오류: {e}")
        return {
            'top_routes': [],
            'chart_labels': [],
            'chart_values': []
        }

def create_table_html(df: pd.DataFrame, max_rows: int = 20, classes: str = 'table table-bordered table-sm') -> str:
    """DataFrame을 HTML 테이블로 변환"""
    try:
        return df.head(max_rows).to_html(classes=classes, index=False)
    except Exception as e:
        print(f"테이블 HTML 생성 오류: {e}")
        return "<p>데이터를 표시할 수 없습니다.</p>"

def validate_route_name(route_name: str) -> bool:
    """노선명 유효성 검사"""
    if not route_name or not route_name.strip():
        return False
    return True

def sanitize_input(input_str: str) -> str:
    """입력값 정리"""
    if not input_str:
        return ""
    return input_str.strip()

def format_error_message(error: Exception) -> str:
    """에러 메시지 포맷팅"""
    if hasattr(error, 'message'):
        return str(error.message)
    return str(error) 