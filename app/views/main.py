from flask import Blueprint, render_template, g, session
from app.controllers.auth_controller import AuthController

bp = Blueprint('main', __name__)
auth_controller = AuthController()

@bp.before_request
def load_logged_in_user():
    """모든 요청 전에 로그인된 사용자 정보를 로드"""
    user_id = session.get('user_id')
    
    if user_id is None:
        g.user = None
    else:
        try:
            g.user = auth_controller.get_user_by_id(user_id)
        except Exception as e:
            print(f"데이터베이스 연결 오류: {e}")
            g.user = None
            session.clear()  # 오류 시 세션 초기화

@bp.route('/')
def home():
    """홈 페이지"""
    return render_template('home.html') 