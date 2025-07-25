import json
from flask import Blueprint, render_template, request
from app.controllers.bus_controller import BusController
from app.controllers.map_controller import MapController
from app.controllers.team2_controller import Team2Controller

bp = Blueprint('teams', __name__)
bus_controller = BusController()
map_controller = MapController()
team2_controller = Team2Controller()

@bp.route('/team1')
def get_team1():
    """Team1 페이지"""
    return render_template('team1.html')

@bp.route('/team2')
def get_team2():
    """Team2 페이지 - 노선별 교통량 분석"""
    try:
        return team2_controller.get_team2_page()
    except Exception as e:
        print(f"Team2 페이지 오류: {e}")
        return render_template('team2_index.html',
                           table="<p>데이터를 불러오는 중 오류가 발생했습니다.</p>",
                           routes=[],
                           selected_route="",
                           chart_labels=json.dumps([]),
                           chart_values=json.dumps([]))

@bp.route('/api/team2/data')
def get_team2_data():
    """Team2 데이터 API"""
    try:
        data = team2_controller.get_team2_data()
        return json.dumps(data, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

@bp.route('/api/team2/route/<route_name>')
def get_team2_route_data(route_name):
    """Team2 특정 노선 데이터 API"""
    try:
        data = team2_controller.get_route_data(route_name)
        return json.dumps(data, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

@bp.route('/api/team2/chart')
def get_team2_chart_data():
    """Team2 차트 데이터 API"""
    try:
        route_name = request.args.get('route')
        data = team2_controller.get_chart_data(route_name)
        return json.dumps(data, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

@bp.route('/team3', methods=['GET', 'POST'])
def get_team3():
    """Team3 페이지"""
    try:
        data = bus_controller.get_team3_data()
        
        return render_template('team3.html',
                           routes=data['routes'],
                           selected=data.get('selected'),
                           error_msg=data.get('error_msg'),
                           labels=json.dumps(data.get('labels', []), ensure_ascii=False),
                           chart_data=json.dumps(data.get('chart_data', []), ensure_ascii=False))
    except Exception as e:
        return render_template('team3.html',
                           routes=[],
                           selected=None,
                           error_msg='서버 오류: ' + str(e),
                           labels=json.dumps([]),
                           chart_data=json.dumps([]))

@bp.route('/team4')
def get_team4():
    """Team4 페이지 - Folium 버스 노선 지도"""
    try:
        data = map_controller.get_team4_data()
        
        return render_template('team4.html', 
                           routes_summary=data['routes_summary'],
                           has_map=data['has_map'],
                           error_message=data.get('error_message'))
    except Exception as e:
        return render_template('team4.html', 
                           routes_summary=[],
                           has_map=False,
                           error_message=str(e))

@bp.route('/team5', methods=['GET', 'POST'])
def get_team5():
    """Team5 회원가입 페이지"""
    from app.schemas.auth_schema import SimpleRegistrationForm
    from app.controllers.auth_controller import AuthController
    
    form = SimpleRegistrationForm()
    auth_controller = AuthController()
    
    if form.validate_on_submit():
        redirect_page = auth_controller.register(form)
        if redirect_page:
            from flask import redirect, url_for
            return redirect(url_for(redirect_page))
    
    return render_template('team5.html', form=form) 