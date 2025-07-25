from typing import Optional, Dict, Any
from flask import session, flash, redirect, url_for, g
from app.services.auth_service import AuthService
from app.schemas.auth_schema import SimpleRegistrationForm, LoginForm

class AuthController:
    """인증 컨트롤러 클래스"""
    
    def __init__(self):
        self.auth_service = AuthService()
    
    def login(self, form: LoginForm) -> Optional[str]:
        """로그인 처리"""
        if form.validate_on_submit():
            user = self.auth_service.authenticate_user(form.username.data, form.password.data)
            if user:
                session.clear()
                session['user_id'] = user['id']
                flash(f'{user["full_name"]}님, 환영합니다!', 'success')
                return 'home'
            else:
                flash('사용자명 또는 비밀번호가 올바르지 않습니다.', 'error')
        
        return None
    
    def logout(self) -> str:
        """로그아웃 처리"""
        if g.user:
            flash(f'{g.user["full_name"]}님, 안전하게 로그아웃되었습니다.', 'info')
        session.clear()
        return 'home'
    
    def register(self, form: SimpleRegistrationForm) -> Optional[str]:
        """회원가입 처리"""
        if form.validate_on_submit():
            try:
                # 데이터 유효성 검사
                self.auth_service.validate_user_data(
                    form.username.data,
                    form.email.data,
                    form.password.data,
                    form.full_name.data
                )
                
                # 사용자 등록
                user_id = self.auth_service.register_user(
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
                return 'home'
                
            except ValueError as e:
                flash(str(e), 'error')
            except Exception as e:
                flash(f'회원가입 중 오류가 발생했습니다: {str(e)}', 'error')
        
        return None
    
    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """현재 로그인된 사용자 조회"""
        user_id = session.get('user_id')
        if user_id is None:
            return None
        
        try:
            return self.auth_service.get_user_by_id(user_id)
        except Exception as e:
            print(f"사용자 조회 오류: {e}")
            session.clear()
            return None
    
    def require_login(self) -> bool:
        """로그인 필요 여부 확인"""
        return session.get('user_id') is not None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """ID로 사용자 조회"""
        return self.auth_service.get_user_by_id(user_id)
    
    def get_all_users(self) -> list:
        """모든 사용자 조회 (관리용)"""
        return self.auth_service.get_all_users() 
