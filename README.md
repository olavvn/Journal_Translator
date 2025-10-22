# PDF 논문 번역기

구글 제미나이 API를 이용한 영어 논문 한국어 번역 애플리케이션입니다.

## ✨ 주요 기능

### 🔄 번역 기능
- 📄 PDF 파일 드래그앤드롭 업로드
- 🤖 구글 제미나이 API를 통한 자동 번역
- 🎯 전체 본문 통번역 (생략 없음)
- 📝 마크다운 형식으로 번역본 생성

### 📱 사용자 인터페이스
- 🖥️ 양쪽 화면 레이아웃 (왼쪽: 원문 PDF, 오른쪽: 번역본)
- 🔍 PDF 뷰어 (터치패드 확대/축소/드래그 지원)
- 📱 반응형 디자인
- 🎨 깔끔한 UI/UX

### 💾 데이터 관리
- 🗄️ SQLite 데이터베이스 기반 번역 기록 저장
- 📚 사이드바 번역 기록 목록
- 🔄 번역 기록 복원 기능
- 🗑️ 번역 기록 삭제 기능
- 🆕 새 번역 생성 기능

### 📥 파일 관리
- 📄 번역본 다운로드 (Markdown 형식)
- 📋 원문+번역본 통합 다운로드
- 💾 PDF와 번역본 쌍으로 저장

## 🚀 설치 및 실행

### 1. 저장소 클론
```bash
git clone <repository-url>
cd 008_Translation_Bot
```

### 2. 가상환경 활성화
```bash
# Windows
myenv\Scripts\activate

# macOS/Linux
source myenv/bin/activate
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 환경 변수 설정
`.env` 파일을 생성하고 구글 제미나이 API 키를 설정하세요:
```bash
# .env 파일 생성
echo GOOGLE_API_KEY=your_google_api_key_here > .env
```

### 5. 애플리케이션 실행
```bash
streamlit run app.py
```

### 6. 브라우저에서 접속
```
Local URL: http://localhost:8501
```

## 📖 사용법

### 🆕 새 번역 시작
1. **새 번역 생성**: 사이드바에서 "📄 새 번역 생성" 버튼 클릭
2. **PDF 업로드**: 왼쪽 화면에 영어 논문 PDF를 드래그앤드롭
3. **번역 시작**: 오른쪽 화면의 "🔄 번역 시작" 버튼 클릭
4. **결과 확인**: 번역된 한국어 텍스트 확인
5. **다운로드**: 번역본을 Markdown 파일로 다운로드

### 📚 번역 기록 관리
1. **기록 확인**: 사이드바에서 번역 기록 목록 확인
2. **기록 복원**: 원하는 번역 기록 클릭하여 복원
3. **기록 삭제**: "🗑️" 버튼으로 번역 기록 삭제

### 🔍 PDF 뷰어 사용법
1. **PDF 보기 방식 선택**: "PDF 뷰어 (권장)", "텍스트 보기", "PDF 뷰어 (HTML iframe)"

## ⚠️ 주의사항

- **API 키 필요**: 구글 제미나이 API 키가 필요합니다
- **통번역**: 번역은 전체 본문을 빠짐없이 수행합니다
- **처리 시간**: 대용량 PDF의 경우 시간이 오래 걸릴 수 있습니다
- **데이터 저장**: 번역 기록은 SQLite 데이터베이스에 저장됩니다

## 🏗️ 프로젝트 구조

```
Journal_Translator/
├── app.py              # 메인 Streamlit 애플리케이션
├── database.py         # SQLite 데이터베이스 관리
├── pdf_processor.py    # PDF 텍스트 추출
├── translator.py       # 구글 제미나이 번역
├── requirements.txt   # 핵심 의존성 목록
├── .env               # 환경 변수 (API 키)
├── .gitignore         # Git 무시 파일
├── README.md          # 프로젝트 문서
├── translations.db     # 번역 기록 데이터베이스
└── myenv/             # 가상환경
```

## 🔧 기술 스택

- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: SQLite
- **AI**: Google Gemini API
- **PDF Processing**: PyPDF2
- **Environment**: python-dotenv

## 📦 핵심 의존성

```
streamlit[pdf]==1.50.0     # 웹 애플리케이션 프레임워크 (PDF 뷰어 포함)
google-generativeai==0.8.5 # 구글 제미나이 API
PyPDF2==3.0.1              # PDF 파일 처리
python-dotenv==1.1.1       # 환경 변수 관리
```

## 🚀 개발 환경 설정

### 가상환경 생성
```bash
python -m venv myenv
myenv\Scripts\activate  # Windows
# source myenv/bin/activate  # macOS/Linux
```

### 의존성 설치
```bash
pip install -r requirements.txt
```

### 환경 변수 설정
```bash
# .env 파일 생성
echo GOOGLE_API_KEY=your_api_key_here > .env
```

### 애플리케이션 실행
```bash
streamlit run app.py
```
