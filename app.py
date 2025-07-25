from flask import Flask, render_template, jsonify, request, send_file, flash, redirect, url_for, session, g
from forms import SimpleRegistrationForm, LoginForm
from app.utils.database import UserDatabase
from app.views.teams import bp as teams_bp
from app.views.main import bp as main_bp
from app.views.auth import bp as auth_bp
from app.views.bus import bp as bus_bp
import requests 
import json
import os
import pandas as pd
from map.map import BusRouteMapper, create_bus_route_map, get_routes_data_summary


app = Flask(
    __name__,
    template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
)
app.register_blueprint(teams_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(bus_bp)
app.register_blueprint(main_bp)

API_KEY = "Q87H6RHMmHu5VIe9CJqbwVioFAV+HE/319+CbDQqB6HgCx8sp4nZafCs+X5eFeY31zuCs0mGyDkeFkRcGxWQjw=="
BASE = "http://apis.data.go.kr/6410000/busrouteservice/v2"
# 데이터베이스 초기화 (CloudType 사용)
db = UserDatabase(use_cloud=True)

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

# Blueprint는 이미 위에서 등록되었으므로 중복 등록을 제거합니다.
# app.register_blueprint(teams_bp)

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
