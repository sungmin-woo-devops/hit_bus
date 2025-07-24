import json
import folium
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class BusRouteMapper:
    """버스 노선 지도 생성 클래스"""
    
    def __init__(self, json_path: str):
        """
        초기화
        
        Args:
            json_path (str): custom_routes.json 파일 경로
        """
        self.json_path = json_path
        self.routes_data = None
        self.map_object = None
        
    def load_routes_data(self) -> Dict:
        """
        JSON 파일에서 노선 데이터 로드
        
        Returns:
            Dict: 로드된 노선 데이터
        """
        try:
            with open(self.json_path, encoding="utf-8") as f:
                self.routes_data = json.load(f)
            print(f"총 {len(self.routes_data)}개의 노선 데이터 로드 완료")
            return self.routes_data
        except FileNotFoundError:
            print(f"파일을 찾을 수 없습니다: {self.json_path}")
            raise
        except json.JSONDecodeError:
            print(f"JSON 파일 형식이 올바르지 않습니다: {self.json_path}")
            raise
    
    def get_routes_summary(self) -> List[Dict]:
        """
        노선별 요약 정보 반환
        
        Returns:
            List[Dict]: 노선별 요약 정보 리스트
        """
        if not self.routes_data:
            self.load_routes_data()
            
        summary = []
        for route_id, route_info in self.routes_data.items():
            summary.append({
                'route_id': route_id,
                'route_no': route_info.get('routeno', 'Unknown'),
                'node_count': len(route_info['nodes'])
            })
        return summary
    
    def create_map(
        self, 
        center_lat: Optional[float] = None, 
        center_lon: Optional[float] = None, 
        zoom_start: int = 12
    ) -> folium.Map:
        """
        버스 노선 지도 생성
        
        Args:
            center_lat: 지도 중심 위도
            center_lon: 지도 중심 경도
            zoom_start: 초기 줌 레벨
            
        Returns:
            folium.Map: 생성된 지도 객체
        """
        if not self.routes_data:
            self.load_routes_data()
        
        # 지도 중심 좌표 설정
        if center_lat is None or center_lon is None:
            first_route = next(iter(self.routes_data.values()))
            first_node = first_route["nodes"][0]
            center_lat = first_node["gpslati"]
            center_lon = first_node["gpslong"]
        
        # 지도 초기화
        self.map_object = folium.Map(
            location=[center_lat, center_lon], 
            zoom_start=zoom_start,
            tiles='OpenStreetMap'
        )
        
        # 다양한 타일 레이어 추가
        self._add_tile_layers()
        
        # 노선 및 정거장 추가
        self._add_routes_and_stops()
        
        # 레이어 컨트롤 추가
        folium.LayerControl().add_to(self.map_object)
        
        return self.map_object
    
    def _add_tile_layers(self):
        """다양한 지도 타일 레이어 추가"""
        tile_layers = [
            ("기본 지도", "OpenStreetMap"),
            ("밝은 지도", "CartoDB positron"),
            ("어두운 지도", "CartoDB dark_matter")
        ]
        
        for name, tile in tile_layers:
            try:
                folium.TileLayer(
                    tiles=tile,
                    attr=name,
                    name=name,
                    overlay=False,
                    control=True
                ).add_to(self.map_object)
            except Exception as e:
                print(f"타일 레이어 추가 실패 ({name}): {e}")
    
    def _add_routes_and_stops(self):
        """노선과 정거장을 지도에 추가"""
        # 노선별 색상 설정
        colors = ['blue', 'red', 'green', 'purple', 'orange', 'darkred', 
                  'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', 
                  'darkpurple', 'pink', 'lightblue', 'lightgreen', 'gray', 
                  'black', 'lightgray']
        
        for idx, (route_id, route_info) in enumerate(self.routes_data.items()):
            color = colors[idx % len(colors)]
            
            # nodes를 nodeord 순으로 정렬
            nodes = sorted(route_info["nodes"], key=lambda x: x["nodeord"])
            
            # 노선 경로 좌표 추출
            coordinates = []
            for node in nodes:
                lat = float(node["gpslati"])
                lon = float(node["gpslong"])
                coordinates.append([lat, lon])
            
            # 노선 경로를 선으로 연결
            folium.PolyLine(
                coordinates,
                color=color,
                weight=3,
                opacity=0.8,
                tooltip=f'노선번호: {route_info.get("routeno", route_id)}'
            ).add_to(self.map_object)
            
            # 각 정거장에 마커 추가
            for node in nodes:
                lat = float(node["gpslati"])
                lon = float(node["gpslong"])
                
                popup_text = f"""
                <b>정거장 정보</b><br>
                노선번호: {route_info.get("routeno", "Unknown")}<br>
                정거장명: {node["nodenm"]}<br>
                정거장ID: {node["nodeid"]}<br>
                순서: {node["nodeord"]}<br>
                좌표: ({lat:.6f}, {lon:.6f})
                """
                
                folium.CircleMarker(
                    location=[lat, lon],
                    radius=4,
                    popup=folium.Popup(popup_text, max_width=300),
                    tooltip=node["nodenm"],
                    color=color,
                    fill=True,
                    fillColor=color,
                    fillOpacity=0.7
                ).add_to(self.map_object)
    
    def save_map(self, output_path: str) -> str:
        """
        지도를 HTML 파일로 저장
        
        Args:
            output_path (str): 저장할 파일 경로
            
        Returns:
            str: 저장된 파일 경로
        """
        if not self.map_object:
            self.create_map()
        
        # 디렉토리 생성
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # 지도 저장
        self.map_object.save(output_path)
        print(f"지도가 저장되었습니다: {output_path}")
        return output_path
    
    def get_map_html(self) -> str:
        """
        지도 HTML 문자열 반환 (임베딩용)
        
        Returns:
            str: 지도 HTML 문자열
        """
        if not self.map_object:
            self.create_map()
        
        return self.map_object._repr_html_()


def create_bus_route_map(
    json_path: str, 
    output_path: str, 
    center_coords: Optional[Tuple[float, float]] = None,
    zoom_start: int = 11
) -> str:
    """
    버스 노선 지도 생성 및 저장 (단일 함수 버전)
    
    Args:
        json_path (str): custom_routes.json 파일 경로
        output_path (str): 저장할 HTML 파일 경로
        center_coords (Optional[Tuple[float, float]]): 지도 중심 좌표 (위도, 경도)
        zoom_start (int): 초기 줌 레벨
        
    Returns:
        str: 저장된 파일 경로
        
    사용 예시:
        create_bus_route_map(
            json_path="bus/map/json/custom_routes.json",
            output_path="bus/static/bus_routes_map.html"
        )
    """
    mapper = BusRouteMapper(json_path)
    
    if center_coords:
        mapper.create_map(center_coords[0], center_coords[1], zoom_start)
    else:
        mapper.create_map(zoom_start=zoom_start)
    
    return mapper.save_map(output_path)


def get_routes_data_summary(json_path: str) -> List[Dict]:
    """
    노선 데이터 요약 정보 반환
    
    Args:
        json_path (str): custom_routes.json 파일 경로
        
    Returns:
        List[Dict]: 노선별 요약 정보
    """
    mapper = BusRouteMapper(json_path)
    return mapper.get_routes_summary()


if __name__ == "__main__":
    # 테스트 실행
    json_file = "json/custom_routes.json"
    output_file = "../static/bus_routes_map.html"
    
    try:
        # 지도 생성 및 저장
        saved_path = create_bus_route_map(json_file, output_file)
        print(f"지도 생성 완료: {saved_path}")
        
        # 요약 정보 출력
        summary = get_routes_data_summary(json_file)
        print("\n=== 노선별 정보 요약 ===")
        for route in summary[:5]:  # 첫 5개만 출력
            print(f"노선 {route['route_no']} (ID: {route['route_id']}): {route['node_count']}개 정거장")
            
    except Exception as e:
        print(f"오류 발생: {e}")
