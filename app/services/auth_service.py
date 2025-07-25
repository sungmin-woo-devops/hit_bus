from typing import Optional, Dict, Any
from app.utils.database import UserDatabase
from app.models.user import User

class AuthService:
    """인증 서비스 클래스"""
    
    def __init__(self):
        self.db = UserDatabase()
    
    def register_user(self, username: str, email: str, password: str, full_name: str,
                     phone: Optional[str] = None, birth_date: Optional[str] = None) -> int:
        """사용자 등록"""
        try:
            user_id = self.db.create_user(
                username=username,
                email=email,
                password=password,
                full_name=full_name,
                phone=phone,
                birth_date=birth_date
            )
            return user_id
        except ValueError as e:
            raise e
        except Exception as e:
            raise ValueError(f"회원가입 중 오류가 발생했습니다: {str(e)}")
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """사용자 인증"""
        try:
            user = self.db.authenticate_user(username, password)
            return user
        except Exception as e:
            print(f"인증 오류: {e}")
            return None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """ID로 사용자 조회"""
        try:
            return self.db.get_user_by_id(user_id)
        except Exception as e:
            print(f"사용자 조회 오류: {e}")
            return None
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """사용자명으로 사용자 조회"""
        try:
            return self.db.get_user_by_username(username)
        except Exception as e:
            print(f"사용자 조회 오류: {e}")
            return None
    
    def get_all_users(self) -> list:
        """모든 사용자 조회 (관리용)"""
        try:
            return self.db.get_all_users()
        except Exception as e:
            print(f"사용자 목록 조회 오류: {e}")
            return []
    
    def validate_user_data(self, username: str, email: str, password: str, full_name: str) -> bool:
        """사용자 데이터 유효성 검사"""
        if not username or len(username) < 3:
            raise ValueError("사용자명은 최소 3자 이상이어야 합니다.")
        
        if not email or '@' not in email:
            raise ValueError("올바른 이메일 형식을 입력해주세요.")
        
        if not password or len(password) < 6:
            raise ValueError("비밀번호는 최소 6자 이상이어야 합니다.")
        
        if not full_name or len(full_name) < 2:
            raise ValueError("이름은 최소 2자 이상이어야 합니다.")
        
        return True 