import os
import json
from typing import Dict, List, Any, Optional
from flask import current_app
from app.utils.helpers import load_json_data, get_static_file_path

class MapService:
    """지도 서비스 클래스"""
    
    def __init__(self):
        self.map_data_path = current_app.config.get('MAP_DATA_PATH', 'map/json/custom_routes.json') if current_app else 'map/json/custom_routes.json'
        self.map_file_path = current_app.config.get('MAP_FILE_PATH', 'static/bus_routes_map.html') if current_app else 'static/bus_routes_map.html'
    
    def get_routes_summary(self) -> List[Dict[str, Any]]:
        """버스 노선 요약 정보 조회"""
        try:
            json_path = os.path.join(os.path.dirname(__file__), '..', '..', self.map_data_path)
            routes_data = load_json_data(json_path)
            
            if not routes_data:
                return []
            
            routes_summary = []
            for route in routes_data.get('routes', []):
                routes_summary.append({
                    'name': route.get('name', 'Unknown'),
                    'stops': len(route.get('stops', [])),
                    'distance': route.get('distance', 0),
                    'type': route.get('type', 'Unknown')
                })
            
            return routes_summary
        except Exception as e:
            print(f"노선 요약 정보 조회 오류: {e}")
            return []
    
    def check_map_file_exists(self) -> bool:
        """지도 파일 존재 여부 확인"""
        try:
            map_file_path = os.path.join(os.path.dirname(__file__), '..', '..', self.map_file_path)
            return os.path.exists(map_file_path)
        except Exception as e:
            print(f"지도 파일 확인 오류: {e}")
            return False
    
    def create_map_file(self) -> bool:
        """지도 파일 생성"""
        try:
            # 여기서 실제 지도 생성 로직을 구현
            # 현재는 기본 HTML 파일 생성
            map_file_path = os.path.join(os.path.dirname(__file__), '..', '..', self.map_file_path)
            os.makedirs(os.path.dirname(map_file_path), exist_ok=True)
            
            with open(map_file_path, 'w', encoding='utf-8') as f:
                f.write("""
<!DOCTYPE html>
<html>
<head>
    <title>버스 노선 지도</title>
</head>
<body>
    <h1>버스 노선 지도</h1>
    <p>지도가 여기에 표시됩니다.</p>
</body>
</html>
                """)
            
            return True
        except Exception as e:
            print(f"지도 파일 생성 오류: {e}")
            return False 