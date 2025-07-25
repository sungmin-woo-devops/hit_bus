"""bus/database.py
프로젝트 구조 개편 후에도 `from database import UserDatabase` 같은 레거시 임포트가
동작하도록 하기 위한 호환성 래퍼입니다. 실제 구현은 `app.utils.database` 모듈에
존재합니다.

이 파일을 삭제해도 무방하지만, 외부 코드나 노트북 등에서의 기존 임포트를
깨뜨리지 않기 위해 래핑 방식을 선택했습니다.
"""

from app.utils.database import (
    UserDatabase,
    create_local_db,
    create_cloud_db,
)

# re-export
__all__ = [
    "UserDatabase",
    "create_local_db",
    "create_cloud_db",
]