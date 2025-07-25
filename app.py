<<<<<<< HEAD
=======
from flask import Flask, render_template, jsonify, request, send_file, flash, redirect, url_for, session, g
from forms import SimpleRegistrationForm, LoginForm
from database import UserDatabase
import requests
>>>>>>> 080a139abd55169e2bf1a453dad0e0be94e68be0
import json
import os
import pandas as pd
import requests
from flask import Flask, render_template, jsonify, request, send_file, flash, redirect, url_for, session, g
from database import UserDatabase
from forms import SimpleRegistrationForm, LoginForm
from map.map import BusRouteMapper, create_bus_route_map, get_routes_data_summary

app = Flask(__name__)
app.secret_key = 'super-secret-key'  # CSRF 보호를 위해 시크릿 키를 설정합니다.

<<<<<<< HEAD
# TEAM1 envs
API_KEY = "Q87H6RHMmHu5VIe9CJqbwVioFAV+HE/319+CbDQqB6HgCx8sp4nZafCs+X5eFeY31zuCs0mGyDkeFkRcGxWQjw=="
BASE = "http://apis.data.go.kr/6410000/busrouteservice/v2"

# 데이터베이스 초기화 (CloudType 사용)
db = UserDatabase(use_cloud=True)
=======
API_KEY = "Q87H6RHMmHu5VIe9CJqbwVioFAV+HE/319+CbDQqB6HgCx8sp4nZafCs+X5eFeY31zuCs0mGyDkeFkRcGxWQjw=="
BASE = "http://apis.data.go.kr/6410000/busrouteservice/v2"
# 데이터베이스 초기화
db = UserDatabase(
    host='localhost',
    user='root',
    password='1111',  # 실제 비밀번호로 변경
    database='test'
)
>>>>>>> 080a139abd55169e2bf1a453dad0e0be94e68be0

@app.before_request
def load_logged_in_user():
    """모든 요청 전에 로그인된 사용자 정보를 로드"""
    user_id = session.get('user_id')
    
    if user_id is None:
        g.user = None
    else:
        try:
            g.user = db.get_user_by_id(user_id)
        except Exception as e:
            print(f"데이터베이스 연결 오류: {e}")
            g.user = None
            session.clear()  # 오류 시 세션 초기화

@app.route('/login', methods=['GET', 'POST'])
def login():
    """로그인 페이지"""
    form = LoginForm()
    
    if form.validate_on_submit():
        user = db.authenticate_user(form.username.data, form.password.data)
        if user:
            session.clear()
            session['user_id'] = user['id']
            flash(f'{user["full_name"]}님, 환영합니다!', 'success')
            return redirect(url_for('home'))
        else:
            flash('사용자명 또는 비밀번호가 올바르지 않습니다.', 'error')
    
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """로그아웃"""
    if g.user:
        flash(f'{g.user["full_name"]}님, 안전하게 로그아웃되었습니다.', 'info')
    session.clear()
    return redirect(url_for('home'))

@app.route('/')
def home():
    return render_template('home.html')

<<<<<<< HEAD
# team1
@app.route('/api/bus', methods=['GET'])
def get_bus():
    """버스 노선 정보 API"""
    try:
        route_name = request.args.get('route')
        if not route_name:
            return jsonify({"error": "route 파라미터가 필요합니다."}), 400

        print(f"버스 노선 검색: {route_name}")

        # 1단계: 노선 목록 조회
        resp1 = requests.get(f"{BASE}/getBusRouteListv2", params={
            'serviceKey': API_KEY,
            'keyword': route_name,
            'format': 'json'
        }, timeout=10)
        
        if resp1.status_code != 200:
            print(f"API 호출 실패 - 상태코드: {resp1.status_code}")
            return jsonify({"error": f"API 호출 실패: {resp1.status_code}"}), 500
            
        data1 = resp1.json().get('response', {}).get('msgBody', {}).get('busRouteList')
        if not data1:
            print(f"노선을 찾을 수 없음: {route_name}")
            return jsonify({"error": "노선을 찾을 수 없습니다."}), 404

        # 노선이 리스트인 경우 첫 번째 항목 선택
        route = data1 if isinstance(data1, dict) else data1[0]
        route_id = route.get('routeId')
        
        if not route_id:
            return jsonify({"error": "노선 ID를 찾을 수 없습니다."}), 404

        print(f"노선 ID 찾음: {route_id}")

        # 2단계: 노선 상세 정보 조회
        resp2 = requests.get(f"{BASE}/getBusRouteInfoItemv2", params={
            'serviceKey': API_KEY,
            'routeId': route_id,
            'format': 'json'
        }, timeout=10)
        
        if resp2.status_code != 200:
            print(f"노선 정보 API 호출 실패 - 상태코드: {resp2.status_code}")
            return jsonify({"error": f"노선 정보 API 호출 실패: {resp2.status_code}"}), 500
            
        info = resp2.json().get('response', {}).get('msgBody', {}).get('busRouteInfoItem')
        if not info:
            print(f"노선 정보가 없음: {route_id}")
            return jsonify({"error": "노선 정보가 없습니다."}), 404

        print(f"노선 정보 조회 성공: {route_name}")
        return jsonify({
            "route": route,
            "info": info
        })

    except requests.exceptions.Timeout:
        print("API 호출 타임아웃")
        return jsonify({"error": "API 응답 시간이 초과되었습니다. 다시 시도해주세요."}), 408
    except requests.exceptions.RequestException as e:
        print(f"API 호출 오류: {e}")
        return jsonify({"error": "외부 API 호출 중 오류가 발생했습니다."}), 500
    except Exception as e:
        print(f"예상치 못한 오류: {e}")
        return jsonify({"error": "서버 내부 오류가 발생했습니다."}), 500

=======



@app.route('/api/bus', methods=['GET'])
def get_bus():
    route_name = request.args.get('route')
    if not route_name:
        return jsonify({"error": "route 파라미터 필요"}), 400

    
    resp1 = requests.get(f"{BASE}/getBusRouteListv2", params={
        'serviceKey': API_KEY,
        'keyword': route_name,
        'format': 'json'
    }, timeout=5)
    resp1.raise_for_status()
    data1 = resp1.json().get('response', {}).get('msgBody', {}).get('busRouteList')
    if not data1:
        return jsonify({"error": "노선을 찾을 수 없습니다."}), 404

    
    route = data1 if isinstance(data1, dict) else data1[0]
    route_id = route.get('routeId')

 
    resp2 = requests.get(f"{BASE}/getBusRouteInfoItemv2", params={
        'serviceKey': API_KEY,
        'routeId': route_id,
        'format': 'json'
    }, timeout=5)
    resp2.raise_for_status()
    info = resp2.json().get('response', {}).get('msgBody', {}).get('busRouteInfoItem')
    if not info:
        return jsonify({"error": "노선 정보가 없습니다."}), 404

    return jsonify({
        "route": route,
        "info": info
    })
>>>>>>> 080a139abd55169e2bf1a453dad0e0be94e68be0

@app.route('/team1')
def get_team1():
    return render_template('team1.html')

@app.route('/team2')
def get_team2():
    try:
        # 데이터 파일 경로
        data_path = os.path.join(os.path.dirname(__file__), 'data', 'gyeonggi_bus_stop_2023.csv')
        
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
        data_path = os.path.join(os.path.dirname(__file__), 'data', 'suwon_bus_stop_2024.csv')
        
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
    """Team4 페이지 - Folium 버스 노선 지도"""
    try:
        # 버스 노선 데이터 요약 정보 가져오기
        json_path = os.path.join(os.path.dirname(__file__), 'map', 'json', 'custom_routes.json')
        routes_summary = get_routes_data_summary(json_path)
        
        # 지도 파일 경로 설정
        map_file_path = os.path.join(os.path.dirname(__file__), 'static', 'bus_routes_map.html')
        
        # 지도 파일이 없으면 생성
        if not os.path.exists(map_file_path):
            create_bus_route_map(json_path, map_file_path)
        
        return render_template('team4.html', 
                             routes_summary=routes_summary,
                             has_map=os.path.exists(map_file_path))
    except Exception as e:
        print(f"Team4 페이지 로드 오류: {e}")
        return render_template('team4.html', 
                             routes_summary=[],
                             has_map=False,
                             error_message=str(e))

@app.route('/team5', methods=['GET', 'POST'])
def get_team5():
    """Team5 회원가입 페이지"""
    form = SimpleRegistrationForm()
    
    if form.validate_on_submit():
        try:
            user_id = db.create_user(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
                full_name=form.full_name.data,
                phone=form.phone.data if form.phone.data else None,
                birth_date=form.birth_date.data if form.birth_date.data else None
            )
            # 회원가입 후 자동 로그인
            session.clear()
            session['user_id'] = user_id
            flash(f'{form.full_name.data}님, 회원가입이 완료되었습니다! 자동으로 로그인되었습니다.', 'success')
            return redirect(url_for('home'))
        except ValueError as e:
            flash(str(e), 'error')
    
    return render_template('team5.html', form=form)

# Folium 지도 관련 API 엔드포인트
@app.route('/api/bus-map')
def get_bus_map():
    """버스 노선 지도 HTML 파일 반환"""
    try:
        map_file_path = os.path.join(os.path.dirname(__file__), 'static', 'bus_routes_map.html')
        
        # 지도 파일이 없으면 생성
        if not os.path.exists(map_file_path):
            json_path = os.path.join(os.path.dirname(__file__), 'map', 'json', 'custom_routes.json')
            create_bus_route_map(json_path, map_file_path)
        
        return send_file(map_file_path)
    except Exception as e:
        return jsonify({"error": f"지도 파일을 찾을 수 없습니다: {str(e)}"}), 404

@app.route('/api/regenerate-bus-map')
def regenerate_bus_map():
    """버스 노선 지도 재생성"""
    try:
        json_path = os.path.join(os.path.dirname(__file__), 'map', 'json', 'custom_routes.json')
        map_file_path = os.path.join(os.path.dirname(__file__), 'static', 'bus_routes_map.html')
        
        # 지도 재생성
        create_bus_route_map(json_path, map_file_path)
        
        return jsonify({
            "success": True,
            "message": "지도가 성공적으로 재생성되었습니다.",
            "map_url": "/api/bus-map"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"지도 생성 실패: {str(e)}"
        }), 500

@app.route('/api/routes-summary')
def get_routes_summary_api():
    """버스 노선 요약 정보 API"""
    try:
        json_path = os.path.join(os.path.dirname(__file__), 'map', 'json', 'custom_routes.json')
        routes_summary = get_routes_data_summary(json_path)
        
        return jsonify({
            "success": True,
            "total_routes": len(routes_summary),
            "routes": routes_summary
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"노선 데이터 로드 실패: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
