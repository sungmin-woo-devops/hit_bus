import os
from datetime import timedelta

class Config:
    """기본 설정 클래스"""
    SECRET_KEY = 'super-secret-key'
    
    # 데이터베이스 설정
    DATABASE_HOST = 'svc.sel5.cloudtype.app'
    DATABASE_PORT = 32134
    DATABASE_USER = 'root'
    DATABASE_PASSWORD = '1111'
    DATABASE_NAME = 'mysql'
    DATABASE_USE_CLOUD = True
    
    # API 설정
    API_KEY = "Q87H6RHMmHu5VIe9CJqbwVioFAV+HE/319+CbDQqB6HgCx8sp4nZafCs+X5eFeY31zuCs0mGyDkeFkRcGxWQjw=="
    BASE_URL = "http://apis.data.go.kr/6410000/busrouteservice/v2"
    
    # 세션 설정
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # 파일 업로드 설정
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'uploads')
    
    # 디버그 설정
    DEBUG = True
    TESTING = False

class DevelopmentConfig(Config):
    """개발 환경 설정"""
    DEBUG = True

class ProductionConfig(Config):
    """운영 환경 설정"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """테스트 환경 설정"""
    TESTING = True
    DEBUG = True 