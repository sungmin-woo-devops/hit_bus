from marshmallow import Schema, fields, validate

class BusRouteSchema(Schema):
    """버스 노선 스키마"""
    route_id = fields.Str(required=True, metadata={"description": "노선 ID"})
    route_name = fields.Str(required=True, metadata={"description": "노선명"})
    route_type = fields.Str(metadata={"description": "노선 타입"})
    start_stop = fields.Str(metadata={"description": "시작 정류장"})
    end_stop = fields.Str(metadata={"description": "종점 정류장"})
    total_distance = fields.Float(metadata={"description": "총 거리"})
    total_time = fields.Int(metadata={"description": "총 소요시간"})

class BusStopSchema(Schema):
    """버스 정류장 스키마"""
    stop_id = fields.Str(required=True, metadata={"description": "정류장 ID"})
    stop_name = fields.Str(required=True, metadata={"description": "정류장명"})
    latitude = fields.Float(required=True, metadata={"description": "위도"})
    longitude = fields.Float(required=True, metadata={"description": "경도"})
    address = fields.Str(metadata={"description": "주소"})
    routes = fields.List(fields.Str(), metadata={"description": "경유 노선"})

class BusRouteRequestSchema(Schema):
    """버스 노선 요청 스키마"""
    route = fields.Str(required=True, validate=validate.Length(min=1), metadata={"description": "검색할 노선명"})

class BusRouteResponseSchema(Schema):
    """버스 노선 응답 스키마"""
    route = fields.Dict(metadata={"description": "노선 정보"})
    info = fields.Dict(metadata={"description": "노선 상세 정보"})

class BusDataRequestSchema(Schema):
    """버스 데이터 요청 스키마"""
    route = fields.Str(metadata={"description": "선택된 노선"})
    time_range = fields.Str(metadata={"description": "시간 범위"})
    date_range = fields.Str(metadata={"description": "날짜 범위"})

class BusDataResponseSchema(Schema):
    """버스 데이터 응답 스키마"""
    routes = fields.List(fields.Str(), metadata={"description": "노선 목록"})
    selected_route = fields.Str(metadata={"description": "선택된 노선"})
    chart_labels = fields.List(fields.Str(), metadata={"description": "차트 라벨"})
    chart_values = fields.List(fields.Float(), metadata={"description": "차트 값"})
    table_html = fields.Str(metadata={"description": "테이블 HTML"}) 