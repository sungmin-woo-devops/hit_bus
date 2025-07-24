# MyBusInfoWeb

버스 정보 웹 애플리케이션

## 프로젝트 개요

이 프로젝트는 Flask와 Jinja2 템플릿을 사용하여 버스 정보를 시각화하는 웹 애플리케이션입니다. D3.js를 사용한 인터랙티브 지도 기능을 포함하고 있습니다.

## 주요 기능

- **D3.js 지도 시각화**: 한국 지도에 버스 정류장과 노선 정보 표시
- **인터랙티브 기능**: 지역 선택, 정류장 클릭, 줌 기능
- **REST API**: 버스 데이터를 JSON 형태로 제공
- **반응형 디자인**: 모바일과 데스크톱 환경 지원

## 기술 스택

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **지도 시각화**: D3.js v7, TopoJSON
- **템플릿 엔진**: Jinja2
- **스타일링**: CSS3 (반응형 디자인)

## 설치 및 실행

### 1. 가상환경 생성 및 활성화

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 가상환경 활성화 (macOS/Linux)
source venv/bin/activate
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 애플리케이션 실행

```bash
python app.py
```

브라우저에서 `http://localhost:5000`으로 접속하세요.

## 프로젝트 구조

```
bus/
├── app.py                 # Flask 메인 애플리케이션
├── requirements.txt       # Python 의존성
├── README.md             # 프로젝트 문서
├── static/
│   ├── css/
│   │   └── style.css     # 메인 스타일시트 (D3.js 지도 스타일 포함)
│   └── js/
│       ├── script.js     # 기본 JavaScript
│       └── d3-map.js     # D3.js 지도 클래스
└── templates/
    ├── base.html         # 기본 템플릿 (D3.js 라이브러리 포함)
    ├── home.html         # 홈페이지
    ├── team1.html        # 팀1 페이지
    ├── team2.html        # 팀2 페이지
    ├── team3.html        # 팀3 페이지
    ├── team4.html        # D3.js 지도 페이지
    └── team5.html        # 팀5 페이지
```

## D3.js 지도 기능

### 주요 기능

1. **한국 지도 표시**: TopoJSON 데이터를 사용한 한국 시도별 지도
2. **버스 정류장 표시**: 빨간색 원형 마커로 정류장 위치 표시
3. **버스 노선 표시**: 녹색 선으로 노선 경로 표시
4. **인터랙티브 기능**:
   - 지역 클릭 시 선택 표시
   - 정류장 호버 시 툴팁 표시
   - 줌 및 패닝 기능
   - 반응형 크기 조정

### API 엔드포인트

- `GET /api/bus-stops`: 버스 정류장 데이터
- `GET /api/bus-routes`: 버스 노선 데이터
- `GET /api/regions`: 지역 정보 데이터
- `GET /api/map-data`: 통합 지도 데이터

### 사용법

1. `/team4` 페이지 접속
2. "지도 로드" 버튼으로 기본 지도 표시
3. "정류장 표시" 버튼으로 버스 정류장 표시
4. "노선 표시" 버튼으로 버스 노선 표시
5. "줌 활성화" 버튼으로 줌 기능 활성화
6. 지역이나 정류장 클릭하여 상세 정보 확인

## 개발 가이드

### 새로운 페이지 추가

1. `templates/` 디렉토리에 새 HTML 파일 생성
2. `base.html`을 상속받아 템플릿 작성
3. `app.py`에 라우트 추가

### D3.js 지도 커스터마이징

1. `static/js/d3-map.js`에서 D3Map 클래스 수정
2. `static/css/style.css`에서 지도 스타일 수정
3. API 엔드포인트에서 데이터 형식 조정

### 데이터 추가

1. `app.py`의 API 엔드포인트에서 데이터 수정
2. 실제 데이터베이스 연결 시 해당 부분 교체
3. CSV 파일이나 JSON 파일에서 데이터 로드 가능

## 브라우저 지원

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 기여하기

1. 이 저장소를 포크하세요
2. 기능 브랜치를 생성하세요 (`git checkout -b feature/AmazingFeature`)
3. 변경사항을 커밋하세요 (`git commit -m 'Add some AmazingFeature'`)
4. 브랜치에 푸시하세요 (`git push origin feature/AmazingFeature`)
5. Pull Request를 생성하세요

## 문의사항

프로젝트에 대한 문의사항이 있으시면 이슈를 생성해 주세요.
