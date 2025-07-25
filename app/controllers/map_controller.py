from typing import Dict, List, Any
from flask import send_file
import os
from app.services.map_service import MapService

class MapController:
    """지도 컨트롤러 클래스"""
    
    def __init__(self):
        self.map_service = MapService()
    
    def get_routes_summary(self) -> List[Dict[str, Any]]:
        """버스 노선 요약 정보 조회"""
        return self.map_service.get_routes_summary()
    
    def get_bus_map_file(self) -> Any:
        """버스 노선 지도 파일 반환"""
        try:
            map_file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'static', 'bus_routes_map.html')
            
            # 지도 파일이 없으면 생성
            if not os.path.exists(map_file_path):
                self.map_service.create_map_file()
            
            return send_file(map_file_path)
        except Exception as e:
            return {"error": f"지도 파일을 찾을 수 없습니다: {str(e)}"}
    
    def regenerate_bus_map(self) -> Dict[str, Any]:
        """버스 노선 지도 재생성"""
        try:
            success = self.map_service.create_map_file()
            
            if success:
                return {
                    "success": True,
                    "message": "지도가 성공적으로 재생성되었습니다.",
                    "map_url": "/api/bus-map"
                }
            else:
                return {
                    "success": False,
                    "error": "지도 생성에 실패했습니다."
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"지도 생성 실패: {str(e)}"
            }
    
    def get_team4_data(self) -> Dict[str, Any]:
        """Team4 데이터 조회"""
        try:
            routes_summary = self.map_service.get_routes_summary()
            has_map = self.map_service.check_map_file_exists()
            
            return {
                'routes_summary': routes_summary,
                'has_map': has_map
            }
        except Exception as e:
            return {
                'routes_summary': [],
                'has_map': False,
                'error_message': str(e)
            } 