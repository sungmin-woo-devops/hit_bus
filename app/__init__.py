from flask import Flask
from flask_wtf.csrf import CSRFProtect
from config.settings import Config

csrf = CSRFProtect()

def create_app(config_class=Config):
    """Flask 애플리케이션 팩토리 함수"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # CSRF 보호 초기화
    csrf.init_app(app)
    
    # 블루프린트 등록
    from app.views import auth, bus, teams, main
    app.register_blueprint(auth.bp)
    app.register_blueprint(bus.bp)
    app.register_blueprint(teams.bp)
    app.register_blueprint(main.bp)
    
    return app 