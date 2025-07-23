<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Flask 웹사이트 프로젝트

이 프로젝트는 Flask를 사용한 다중 페이지 웹사이트입니다.

## 프로젝트 구조
- `app.py`: Flask 애플리케이션 메인 파일
- `templates/`: HTML 템플릿 파일들
- `static/`: CSS, JavaScript, 이미지 등 정적 파일들
- `requirements.txt`: 필요한 Python 패키지 목록

## 코딩 스타일 가이드라인
- Flask 라우트는 명확하고 RESTful하게 작성
- HTML 템플릿은 Jinja2 템플릿 엔진 사용
- CSS는 반응형 디자인을 고려하여 작성
- JavaScript는 ES6+ 문법 사용 권장
- 한국어 콘텐츠를 포함하므로 UTF-8 인코딩 유지

## 기능 요구사항
- 헤더에 5개의 메뉴 항목 (홈, 소개, 서비스, 제품, 연락처)
- 반응형 네비게이션 (모바일 햄버거 메뉴)
- 각 페이지별 고유한 콘텐츠
- 연락처 폼 기능
