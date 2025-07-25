from flask import Blueprint, request, jsonify
from app.controllers.bus_controller import BusController
from app.controllers.map_controller import MapController

bp = Blueprint('bus', __name__, url_prefix='/api')
bus_controller = BusController()
map_controller = MapController()

@bp.route('/bus', methods=['GET'])
def get_bus():
    """버스 노선 정보 API"""
    route_name = request.args.get('route')
    if not route_name:
        return jsonify({"error": "route 파라미터가 필요합니다."}), 400
    
    result = bus_controller.get_bus_route_info(route_name)
    
    if "error" in result:
        return jsonify(result), 400 if "필요합니다" in result["error"] else 500
    
    return jsonify(result)

# Folium 지도 관련 API 엔드포인트
@bp.route('/bus-map')
def get_bus_map():
    """버스 노선 지도 HTML 파일 반환"""
    return map_controller.get_bus_map_file()

@bp.route('/regenerate-bus-map')
def regenerate_bus_map():
    """버스 노선 지도 재생성"""
    result = map_controller.regenerate_bus_map()
    return jsonify(result)

@bp.route('/routes-summary')
def get_routes_summary_api():
    """버스 노선 요약 정보 API"""
    routes_summary = map_controller.get_routes_summary()
    
    return jsonify({
        "success": True,
        "total_routes": len(routes_summary),
        "routes": routes_summary
    }) 