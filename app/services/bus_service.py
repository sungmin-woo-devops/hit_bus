import requests
import pandas as pd
from typing import Dict, List, Any, Optional
from flask import current_app
from app.utils.helpers import load_csv_data, format_bus_data, create_table_html, validate_route_name

class BusService:
    """버스 서비스 클래스"""
    
    def __init__(self):
        self.api_key = current_app.config.get('API_KEY') if current_app else "Q87H6RHMmHu5VIe9CJqbwVioFAV+HE/319+CbDQqB6HgCx8sp4nZafCs+X5eFeY31zuCs0mGyDkeFkRcGxWQjw=="
        self.base_url = current_app.config.get('BASE_URL') if current_app else "http://apis.data.go.kr/6410000/busrouteservice/v2"
    
    def get_bus_route_info(self, route_name: str) -> Dict[str, Any]:
        """버스 노선 정보 조회"""
        try:
            if not validate_route_name(route_name):
                return {"error": "route 파라미터가 필요합니다."}
            
            print(f"버스 노선 검색: {route_name}")
            
            # 1단계: 노선 목록 조회
            resp1 = requests.get(f"{self.base_url}/getBusRouteListv2", params={
                'serviceKey': self.api_key,
                'keyword': route_name,
                'format': 'json'
            }, timeout=10)
            
            if resp1.status_code != 200:
                print(f"API 호출 실패 - 상태코드: {resp1.status_code}")
                return {"error": f"API 호출 실패: {resp1.status_code}"}
                
            data1 = resp1.json().get('response', {}).get('msgBody', {}).get('busRouteList')
            if not data1:
                print(f"노선을 찾을 수 없음: {route_name}")
                return {"error": "노선을 찾을 수 없습니다."}
            
            # 노선이 리스트인 경우 첫 번째 항목 선택
            route = data1 if isinstance(data1, dict) else data1[0]
            route_id = route.get('routeId')
            
            if not route_id:
                return {"error": "노선 ID를 찾을 수 없습니다."}
            
            print(f"노선 ID 찾음: {route_id}")
            
            # 2단계: 노선 상세 정보 조회
            resp2 = requests.get(f"{self.base_url}/getBusRouteInfoItemv2", params={
                'serviceKey': self.api_key,
                'routeId': route_id,
                'format': 'json'
            }, timeout=10)
            
            if resp2.status_code != 200:
                print(f"노선 정보 API 호출 실패 - 상태코드: {resp2.status_code}")
                return {"error": f"노선 정보 API 호출 실패: {resp2.status_code}"}
                
            info = resp2.json().get('response', {}).get('msgBody', {}).get('busRouteInfoItem')
            if not info:
                print(f"노선 정보가 없음: {route_id}")
                return {"error": "노선 정보가 없습니다."}
            
            print(f"노선 정보 조회 성공: {route_name}")
            return {
                "route": route,
                "info": info
            }
            
        except requests.exceptions.Timeout:
            print("API 호출 타임아웃")
            return {"error": "API 응답 시간이 초과되었습니다. 다시 시도해주세요."}
        except requests.exceptions.RequestException as e:
            print(f"API 호출 오류: {e}")
            return {"error": "외부 API 호출 중 오류가 발생했습니다."}
        except Exception as e:
            print(f"예상치 못한 오류: {e}")
            return {"error": "서버 내부 오류가 발생했습니다."}
    
    def get_team2_data(self, selected_route: Optional[str] = None) -> Dict[str, Any]:
        """Team2 데이터 조회"""
        try:
            # 데이터 파일 경로
            data_path = current_app.config.get('DATA_PATH', 'data/gyeonggi_bus_stop_2023.csv')
            
            # CSV 파일 읽기
            df = load_csv_data(data_path)
            if df.empty:
                return self._get_default_team2_data()
            
            # 상위 4개 노선 추출
            top_routes = df['노선'].value_counts().head(4).index.tolist()
            
            # 선택된 노선 (기본값: 첫 번째 노선)
            if not selected_route or selected_route not in top_routes:
                selected_route = top_routes[0] if top_routes else ""
            
            # 선택된 노선 데이터 필터링
            filtered_df = df[df['노선'] == selected_route]
            
            # 테이블 HTML 생성
            table_html = create_table_html(filtered_df, 20, 'team2-table table-bordered table-sm')
            
            # 차트 데이터 포맷팅
            chart_data = format_bus_data(filtered_df)
            
            return {
                'table': table_html,
                'routes': top_routes,
                'selected_route': selected_route,
                'chart_labels': chart_data['chart_labels'],
                'chart_values': chart_data['chart_values']
            }
            
        except Exception as e:
            print(f"Team2 데이터 조회 오류: {e}")
            return self._get_default_team2_data()
    
    def get_team3_data(self, selected_route: Optional[str] = None) -> Dict[str, Any]:
        """Team3 데이터 조회"""
        try:
            # 데이터 파일 경로
            data_path = current_app.config.get('TEAM3_DATA_PATH', 'data/suwon_bus_stop_2024.csv')
            
            # CSV 파일 읽기
            df = load_csv_data(data_path)
            if df.empty:
                return self._get_default_team3_data()
            
            routes = df['노선'].unique().tolist()
            
            if not selected_route:
                return {
                    'routes': routes,
                    'selected': None,
                    'labels': [],
                    'chart_data': []
                }
            
            if selected_route not in routes:
                return {
                    'routes': routes,
                    'selected': None,
                    'error_msg': '노선을 선택해주세요.',
                    'labels': [],
                    'chart_data': []
                }
            
            # 선택된 노선 데이터 필터링
            filtered_df = df[df['노선'] == selected_route]
            temp = filtered_df.groupby(['일시', '월', '시간범위'])['이용객수'].sum().reset_index()
            
            # Chart.js 형식으로 데이터 준비
            chart_data = temp.groupby('월').apply(
                lambda g: {
                    'label': f"{g.name}월",
                    'data': g.sort_values('시간범위')['이용객수'].tolist()
                }
            ).tolist()
            labels = sorted(temp['시간범위'].unique())
            
            return {
                'selected': selected_route,
                'routes': routes,
                'labels': labels,
                'chart_data': chart_data
            }
            
        except Exception as e:
            print(f"Team3 데이터 조회 오류: {e}")
            return self._get_default_team3_data()
    
    def _get_default_team2_data(self) -> Dict[str, Any]:
        """Team2 기본 데이터"""
        return {
            'table': "<p>데이터를 불러오는 중 오류가 발생했습니다.</p>",
            'routes': [],
            'selected_route': "",
            'chart_labels': [],
            'chart_values': []
        }
    
    def _get_default_team3_data(self) -> Dict[str, Any]:
        """Team3 기본 데이터"""
        return {
            'routes': [],
            'selected': None,
            'error_msg': '서버 오류가 발생했습니다.',
            'labels': [],
            'chart_data': []
        } 