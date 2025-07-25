from flask import Flask
from flask_wtf.csrf import CSRFProtect
from config.settings import Config
import os
from jinja2 import ChoiceLoader, FileSystemLoader

csrf = CSRFProtect()

def create_app(config_class=Config):
    """Flask 애플리케이션 팩토리 함수"""
    # 앱 루트: bus/app/, 정적 파일 폴더를 프로젝트 루트의 static 으로 지정
    app = Flask(
        __name__,
        static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static')),
        static_url_path='/static'
    )
    app.config.from_object(config_class)
    
    # CSRF 보호 초기화
    csrf.init_app(app)

    # -----------------------------
    # 추가 템플릿 경로 설정
    # 기본 로더(bus/app/templates)에 더해
    # 프로젝트 루트의 templates(bus/templates)를 함께 검색하도록 구성
    # -----------------------------
    root_template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    if os.path.isdir(root_template_dir):
        app.jinja_loader = ChoiceLoader([
            app.jinja_loader,
            FileSystemLoader(root_template_dir),
        ])
    # -----------------------------
    
    # 블루프린트 등록
    from app.views import auth, bus, teams, main
    app.register_blueprint(auth.bp)
    app.register_blueprint(bus.bp)
    app.register_blueprint(teams.bp)
    app.register_blueprint(main.bp)
    
    return app 