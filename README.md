# Flask 홈페이지 템플릿

헤더에 5개의 메뉴바가 있는 파이썬 Flask 기반 웹사이트 템플릿입니다.

## 기능

- **반응형 네비게이션**: 데스크톱과 모바일에서 모두 작동하는 네비게이션 메뉴
- **5개의 페이지**: 홈, 소개, 서비스, 제품, 연락처
- **현대적인 디자인**: CSS Grid와 Flexbox를 활용한 반응형 레이아웃
- **인터랙티브 요소**: JavaScript를 통한 동적 기능
- **연락처 폼**: 사용자 입력 검증 기능이 포함된 연락처 양식

## 프로젝트 구조

```
bus/
├── app.py                 # Flask 메인 애플리케이션
├── requirements.txt       # Python 의존성
├── templates/            # Jinja2 HTML 템플릿
│   ├── base.html         # 기본 템플릿
│   ├── home.html         # 홈페이지
│   ├── about.html        # 소개 페이지
│   ├── services.html     # 서비스 페이지
│   ├── products.html     # 제품 페이지
│   └── contact.html      # 연락처 페이지
├── static/              # 정적 파일
│   ├── css/
│   │   └── style.css    # 메인 스타일시트
│   └── js/
│       └── script.js    # JavaScript 기능
└── .github/
    └── copilot-instructions.md
```

## 설치 및 실행

### 1. 가상환경 생성 (권장)
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 애플리케이션 실행
```bash
python app.py
```

애플리케이션이 실행되면 http://localhost:5000에서 확인할 수 있습니다.

## 페이지 구성

- **홈** (`/`): 웰컴 메시지와 주요 특징 소개
- **소개** (`/about`): 회사 미션, 비전, 가치 소개
- **서비스** (`/services`): 제공하는 서비스 목록
- **제품** (`/products`): 제품 카탈로그
- **연락처** (`/contact`): 연락 정보 및 문의 폼

## 커스터마이징

### 색상 변경
`static/css/style.css` 파일에서 CSS 변수를 수정하여 색상 테마를 변경할 수 있습니다.

### 콘텐츠 수정
각 HTML 템플릿 파일을 편집하여 콘텐츠를 원하는 대로 수정할 수 있습니다.

### 새 페이지 추가
1. `app.py`에 새 라우트 추가
2. `templates/` 폴더에 새 HTML 템플릿 생성
3. 네비게이션 메뉴에 링크 추가 (`base.html`)

## 기술 스택

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **템플릿 엔진**: Jinja2
- **스타일링**: CSS Grid, Flexbox
- **반응형 디자인**: Mobile-first approach

## 라이선스

이 프로젝트는 MIT 라이선스 하에 제공됩니다.
