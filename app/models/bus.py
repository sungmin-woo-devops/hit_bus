from typing import List, Dict, Any, Optional
from datetime import datetime

class BusRoute:
    """버스 노선 모델 클래스"""
    
    def __init__(self, route_id: str, route_name: str, route_type: str,
                 start_stop: str, end_stop: str, total_distance: Optional[float] = None,
                 total_time: Optional[int] = None, created_at: Optional[datetime] = None):
        self.route_id = route_id
        self.route_name = route_name
        self.route_type = route_type
        self.start_stop = start_stop
        self.end_stop = end_stop
        self.total_distance = total_distance
        self.total_time = total_time
        self.created_at = created_at or datetime.now()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BusRoute':
        """딕셔너리에서 BusRoute 객체 생성"""
        return cls(
            route_id=data.get('routeId'),
            route_name=data.get('routeName'),
            route_type=data.get('routeType'),
            start_stop=data.get('startStop'),
            end_stop=data.get('endStop'),
            total_distance=data.get('totalDistance'),
            total_time=data.get('totalTime'),
            created_at=data.get('created_at')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """BusRoute 객체를 딕셔너리로 변환"""
        return {
            'routeId': self.route_id,
            'routeName': self.route_name,
            'routeType': self.route_type,
            'startStop': self.start_stop,
            'endStop': self.end_stop,
            'totalDistance': self.total_distance,
            'totalTime': self.total_time,
            'created_at': self.created_at
        }
    
    def __repr__(self):
        return f"<BusRoute {self.route_name}>"

class BusStop:
    """버스 정류장 모델 클래스"""
    
    def __init__(self, stop_id: str, stop_name: str, latitude: float, longitude: float,
                 address: str, routes: List[str] = None, created_at: Optional[datetime] = None):
        self.stop_id = stop_id
        self.stop_name = stop_name
        self.latitude = latitude
        self.longitude = longitude
        self.address = address
        self.routes = routes or []
        self.created_at = created_at or datetime.now()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BusStop':
        """딕셔너리에서 BusStop 객체 생성"""
        return cls(
            stop_id=data.get('id'),
            stop_name=data.get('name'),
            latitude=data.get('lat'),
            longitude=data.get('lng'),
            address=data.get('address'),
            routes=data.get('routes', []),
            created_at=data.get('created_at')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """BusStop 객체를 딕셔너리로 변환"""
        return {
            'id': self.stop_id,
            'name': self.stop_name,
            'lat': self.latitude,
            'lng': self.longitude,
            'address': self.address,
            'routes': self.routes,
            'created_at': self.created_at
        }
    
    def __repr__(self):
        return f"<BusStop {self.stop_name}>" 