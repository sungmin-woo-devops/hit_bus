from datetime import datetime
from typing import Optional, Dict, Any
from app.utils.database import UserDatabase

class User:
    """사용자 모델 클래스"""
    
    def __init__(self, id: int, username: str, email: str, full_name: str, 
                 phone: Optional[str] = None, birth_date: Optional[datetime] = None,
                 created_at: Optional[datetime] = None):
        self.id = id
        self.username = username
        self.email = email
        self.full_name = full_name
        self.phone = phone
        self.birth_date = birth_date
        self.created_at = created_at or datetime.now()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """딕셔너리에서 User 객체 생성"""
        return cls(
            id=data.get('id'),
            username=data.get('username'),
            email=data.get('email'),
            full_name=data.get('full_name'),
            phone=data.get('phone'),
            birth_date=data.get('birth_date'),
            created_at=data.get('created_at')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """User 객체를 딕셔너리로 변환"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'phone': self.phone,
            'birth_date': self.birth_date,
            'created_at': self.created_at
        }
    
    def __repr__(self):
        return f"<User {self.username}>" 