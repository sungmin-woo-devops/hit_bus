from typing import Dict, Any, Optional
from flask import request
from app.services.bus_service import BusService
from app.services.data_service import DataService

class BusController:
    """버스 컨트롤러 클래스"""
    
    def __init__(self):
        self.bus_service = BusService()
        self.data_service = DataService()
    
    def get_bus_route_info(self, route_name: str) -> Dict[str, Any]:
        """버스 노선 정보 조회"""
        return self.bus_service.get_bus_route_info(route_name)
    
    def get_team2_data(self) -> Dict[str, Any]:
        """Team2 데이터 조회"""
        selected_route = request.args.get('route')
        return self.bus_service.get_team2_data(selected_route)
    
    def get_team3_data(self) -> Dict[str, Any]:
        """Team3 데이터 조회"""
        if request.method == 'GET':
            # GET 요청: 노선 선택 페이지
            routes = self.data_service.get_available_routes('team3')
            return {
                'routes': routes,
                'selected': None,
                'labels': [],
                'chart_data': []
            }
        else:
            # POST 요청: 선택된 노선 분석
            selected = request.form.get('route')
            routes = self.data_service.get_available_routes('team3')
            
            if not selected:
                return {
                    'routes': routes,
                    'selected': None,
                    'error_msg': '노선을 선택해주세요.',
                    'labels': [],
                    'chart_data': []
                }
            
            return self.bus_service.get_team3_data(selected)
    
    def get_route_statistics(self, route_name: str, data_type: str = 'team2') -> Dict[str, Any]:
        """노선 통계 조회"""
        return self.data_service.get_route_statistics(route_name, data_type)
    
    def get_top_routes(self, data_type: str = 'team2', top_n: int = 5) -> list:
        """상위 노선 조회"""
        return self.data_service.get_top_routes(data_type, top_n)
    
    def get_data_summary(self, data_type: str = 'team2') -> Dict[str, Any]:
        """데이터 요약 조회"""
        return self.data_service.get_data_summary(data_type)
    
    def validate_route_request(self, route_name: str) -> bool:
        """노선 요청 유효성 검사"""
        if not route_name or not route_name.strip():
            return False
        return True 