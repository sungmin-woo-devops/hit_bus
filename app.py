from flask import Flask, render_template, jsonify, request
import json
import os
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/team1')
def get_team1():
    return render_template('team1.html')

@app.route('/team2')
def get_team2():
    try:
        # 데이터 파일 경로
        data_path = os.path.join(os.path.dirname(__file__), 'data', 'bus_data.csv')
        
        # CSV 파일 읽기
        df = pd.read_csv(data_path)
        
        # 상위 4개 노선 추출
        top_routes = df['노선'].value_counts().head(4).index.tolist()
        
        # 선택된 노선 (기본값: 첫 번째 노선)
        selected_route = request.args.get('route') or top_routes[0]
        
        # 선택된 노선 데이터 필터링
        filtered_df = df[df['노선'] == selected_route]
        
        # 테이블 HTML 생성
        table_html = filtered_df.head(20).to_html(classes='team2-table table-bordered table-sm', index=False)
        
        # 시간대별 평균 이용객수 계산
        filtered_df['시작시'] = filtered_df['시간'].str.extract(r'(\d+)').astype(int)
        grouped = filtered_df.groupby('시작시')['이용객수'].mean().sort_index()
        
        # Chart.js에 넘길 JSON 데이터
        chart_labels = list(grouped.index)
        chart_values = list(grouped.values)
        
        return render_template('team2.html',
                               table=table_html,
                               routes=top_routes,
                               selected_route=selected_route,
                               chart_labels=json.dumps(chart_labels),
                               chart_values=json.dumps(chart_values))
    except Exception as e:
        # 에러 발생 시 기본 템플릿 반환
        return render_template('team2.html',
                               table="<p>데이터를 불러오는 중 오류가 발생했습니다.</p>",
                               routes=[],
                               selected_route="",
                               chart_labels=json.dumps([]),
                               chart_values=json.dumps([]))

@app.route('/team3', methods=['GET', 'POST'])
def get_team3():
    try:
        # 데이터 파일 경로
        data_path = os.path.join(os.path.dirname(__file__), 'data', 'df_suwon_flask.csv')
        
        # CSV 파일 읽기
        df = pd.read_csv(data_path)
        
        # GET 요청: 노선 선택 페이지
        if request.method == 'GET':
            routes = df['노선'].unique().tolist()
            return render_template('team3.html', routes=routes, selected=None)
        
        # POST 요청: 선택된 노선 분석
        else:
            selected = request.form.get('route')
            routes = df['노선'].unique().tolist()
            if not selected:
                return render_template(
                    'team3.html',
                    routes=routes,
                    selected=None,
                    error_msg='노선을 선택해주세요.',
                    labels=json.dumps([]),
                    chart_data=json.dumps([])
                )
            
            # 선택된 노선 데이터 필터링
            filtered_df = df[df['노선'] == selected]
            temp = filtered_df.groupby(['일시', '월', '시간범위'])['이용객수'].sum().reset_index()
            
            # Chart.js 형식으로 데이터 준비
            chart_data = temp.groupby('월').apply(
                lambda g: {
                    'label': f"{g.name}월",
                    'data': g.sort_values('시간범위')['이용객수'].tolist()
                }
            ).tolist()
            labels = sorted(temp['시간범위'].unique())
            
            return render_template(
                'team3.html',
                selected=selected,
                routes=routes,
                labels=json.dumps(labels, ensure_ascii=False),
                chart_data=json.dumps(chart_data, ensure_ascii=False)
            )
            
    except Exception as e:
        # 에러 발생 시 기본 템플릿 반환
        return render_template('team3.html',
                               routes=[],
                               selected=None,
                               error_msg='서버 오류: ' + str(e),
                               labels=json.dumps([]),
                               chart_data=json.dumps([]))

@app.route('/team4')
def get_team4():
    return render_template('team4.html')

@app.route('/team5')
def get_team5():
    return render_template('team5.html')

# D3.js 지도 API 엔드포인트
@app.route('/api/bus-stops')
def get_bus_stops():
    """버스 정류장 데이터 API"""
    # 샘플 데이터 (실제로는 데이터베이스에서 가져옴)
    bus_stops = [
        {
            "id": 1,
            "name": "수원시청",
            "lat": 37.2636,
            "lng": 127.0286,
            "routes": 15,
            "address": "경기도 수원시 팔달구 효원로 241"
        },
        {
            "id": 2,
            "name": "수원역",
            "lat": 37.2659,
            "lng": 127.0001,
            "routes": 23,
            "address": "경기도 수원시 팔달구 경수대로 269"
        },
        {
            "id": 3,
            "name": "수원고등학교",
            "lat": 37.2800,
            "lng": 127.0150,
            "routes": 8,
            "address": "경기도 수원시 팔달구 창룡대로 103"
        },
        {
            "id": 4,
            "name": "수원시민공원",
            "lat": 37.2750,
            "lng": 127.0200,
            "routes": 12,
            "address": "경기도 수원시 팔달구 창룡대로 103"
        },
        {
            "id": 5,
            "name": "수원종합운동장",
            "lat": 37.2900,
            "lng": 127.0100,
            "routes": 6,
            "address": "경기도 수원시 팔달구 창룡대로 103"
        }
    ]
    return jsonify(bus_stops)

@app.route('/api/bus-routes')
def get_bus_routes():
    """버스 노선 데이터 API"""
    # 샘플 데이터 (실제로는 데이터베이스에서 가져옴)
    bus_routes = [
        {
            "id": 1,
            "name": "수원시청 ↔ 수원역",
            "coordinates": [[127.0286, 37.2636], [127.0001, 37.2659]],
            "stops": 8,
            "type": "시내버스",
            "frequency": "10분"
        },
        {
            "id": 2,
            "name": "수원고등학교 ↔ 수원시민공원",
            "coordinates": [[127.0150, 37.2800], [127.0200, 37.2750]],
            "stops": 5,
            "type": "마을버스",
            "frequency": "15분"
        },
        {
            "id": 3,
            "name": "수원종합운동장 ↔ 수원시청",
            "coordinates": [[127.0100, 37.2900], [127.0286, 37.2636]],
            "stops": 12,
            "type": "시내버스",
            "frequency": "20분"
        }
    ]
    return jsonify(bus_routes)

@app.route('/api/regions')
def get_regions():
    """지역 데이터 API"""
    # 샘플 데이터 (실제로는 데이터베이스에서 가져옴)
    regions = [
        {
            "id": 1,
            "name": "수원시",
            "code": "41110",
            "population": 1200000,
            "area": 121.0
        },
        {
            "id": 2,
            "name": "성남시",
            "code": "41130",
            "population": 950000,
            "area": 141.8
        },
        {
            "id": 3,
            "name": "용인시",
            "code": "41460",
            "population": 1100000,
            "area": 591.3
        }
    ]
    return jsonify(regions)

@app.route('/api/map-data')
def get_map_data():
    """통합 지도 데이터 API"""
    try:
        # 실제 데이터 파일이 있다면 여기서 로드
        # data_file = os.path.join(app.root_path, 'data', 'map_data.json')
        # with open(data_file, 'r', encoding='utf-8') as f:
        #     data = json.load(f)
        
        # 샘플 통합 데이터
        data = {
            "bus_stops": [
                {"name": "수원시청", "lat": 37.2636, "lng": 127.0286, "routes": 15},
                {"name": "수원역", "lat": 37.2659, "lng": 127.0001, "routes": 23},
                {"name": "수원고등학교", "lat": 37.2800, "lng": 127.0150, "routes": 8}
            ],
            "bus_routes": [
                {
                    "name": "수원시청 ↔ 수원역",
                    "coordinates": [[127.0286, 37.2636], [127.0001, 37.2659]],
                    "stops": 8
                }
            ],
            "statistics": {
                "total_stops": 150,
                "total_routes": 45,
                "total_vehicles": 280
            }
        }
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
