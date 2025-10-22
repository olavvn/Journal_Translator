import streamlit as st
import io
import base64
from pdf_processor import extract_text_from_pdf
from translator import translate_text
from database import TranslationDatabase
import PyPDF2  # PyPDF2 임포트 추가
import time

# 페이지 설정
st.set_page_config(
    page_title="PDF 번역기",
    page_icon="📄",
    layout="wide"
)

# 제목
st.title("📄 PDF 논문 번역기")
st.markdown("---")

# 데이터베이스 초기화
db = TranslationDatabase()

# 세션 상태 초기화
if 'original_text' not in st.session_state:
    st.session_state.original_text = ""
if 'translated_text' not in st.session_state:
    st.session_state.translated_text = ""
if 'pdf_uploaded' not in st.session_state:
    st.session_state.pdf_uploaded = False
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'current_translation_id' not in st.session_state:
    st.session_state.current_translation_id = None
if 'is_loading_from_db' not in st.session_state:
    st.session_state.is_loading_from_db = False

# 메인 레이아웃
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📄 원문 PDF")
    
    # PDF 업로드 (데이터베이스에서 불러온 경우가 아닐 때만 표시)
    if not st.session_state.is_loading_from_db:
        uploaded_file = st.file_uploader(
            "PDF 파일을 드래그앤드롭하거나 선택하세요",
            type=['pdf'],
            help="번역할 영어 논문 PDF를 업로드하세요"
        )
    else:
        uploaded_file = None
    
    if uploaded_file is not None and not st.session_state.is_loading_from_db:
        try:
            # PDF 텍스트 추출
            with st.spinner("PDF에서 텍스트를 추출하는 중..."):
                # .read()를 호출하면 포인터가 파일 끝으로 이동합니다.
                # 추출 함수가 파일을 다시 읽어야 할 수 있으므로 .seek(0)가 필요할 수 있습니다.
                uploaded_file.seek(0)
                extracted_text = extract_text_from_pdf(uploaded_file)
                st.session_state.original_text = extracted_text
                st.session_state.pdf_uploaded = True
                st.session_state.uploaded_file = uploaded_file
                st.session_state.is_loading_from_db = False  # 새로운 파일 업로드
            
            st.success("PDF 텍스트 추출 완료!")
            
            # PDF 파일을 바이트로 읽기 (st.pdf() 또는 base64 인코딩용)
            # 텍스트 추출 후 포인터가 끝에 있을 수 있으므로 다시 0으로 이동
            uploaded_file.seek(0)            
            pdf_bytes = uploaded_file.read()
            
            # PDF 뷰어 옵션 제공
            view_option = st.radio(
                "PDF 보기 방식 선택:",
                ["PDF 뷰어 (권장)", "텍스트 보기", "PDF 뷰어 (HTML iframe)"],
                horizontal=True,
                index=0 # 기본으로 'PDF 뷰어 (권장)' 선택
            )
            
            if view_option == "PDF 뷰어 (권장)":
                # --- 해결 방법 2: Streamlit 기본 st.pdf() 사용 (가장 안정적) ---
                # st.pdf()는 바이트 데이터를 직접 받습니다.
                # height 매개변수로 높이를 조절할 수 있습니다.
                st.pdf(pdf_bytes, height=600)
            
            elif view_option == "PDF 뷰어 (HTML iframe)":
                # --- 해결 방법 1: <embed> 대신 <iframe> 사용 ---
                
                # PDF 파일을 base64로 인코딩
                base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
                
                # iframe을 사용한 PDF 뷰어 (터치패드 확대/축소 및 마우스 드래그 지원)
                pdf_container = f"""
                <div style="
                    height: 600px; 
                    overflow: auto; 
                    border: 1px solid #ddd; 
                    border-radius: 5px;
                    background-color: #f8f9fa;
                ">
                    <iframe 
                        src="data:application/pdf;base64,{base64_pdf}#toolbar=1&navpanes=1&scrollbar=1&zoom=100" 
                        width="100%" 
                        height="100%" 
                        type="application/pdf"
                        style="border: none;"
                        allowfullscreen
                    >
                    </iframe>
                </div>
                """
                st.markdown(pdf_container, unsafe_allow_html=True)
            else:
                # 텍스트 보기
                st.text_area(
                    "추출된 원문 텍스트",
                    value=extracted_text,
                    height=600,
                    disabled=True
                )
            
        except Exception as e:
            st.error(f"PDF 처리 중 오류가 발생했습니다: {str(e)}")
    
    # 데이터베이스에서 불러온 번역 기록이 있는 경우 PDF 뷰어 표시
    if st.session_state.is_loading_from_db and st.session_state.uploaded_file:
        try:
            # 데이터베이스에서 불러온 PDF 파일 처리
            pdf_bytes = st.session_state.uploaded_file.read()
            st.session_state.uploaded_file.seek(0)  # 포인터 리셋
            
            st.success("번역 기록에서 PDF를 불러왔습니다!")
            
            # PDF 뷰어 옵션 제공
            view_option = st.radio(
                "PDF 보기 방식 선택:",
                ["PDF 뷰어 (권장)", "텍스트 보기", "PDF 뷰어 (HTML iframe)"],
                horizontal=True,
                index=0 # 기본으로 'PDF 뷰어 (권장)' 선택
            )
            
            if view_option == "PDF 뷰어 (권장)":
                st.pdf(pdf_bytes, height=600)
            
            elif view_option == "PDF 뷰어 (HTML iframe)":
                # PDF 파일을 base64로 인코딩
                base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
                
                # iframe을 사용한 PDF 뷰어 (터치패드 확대/축소 및 마우스 드래그 지원)
                pdf_container = f"""
                <div style="
                    height: 600px; 
                    overflow: auto; 
                    border: 1px solid #ddd; 
                    border-radius: 5px;
                    background-color: #f8f9fa;
                ">
                    <iframe 
                        src="data:application/pdf;base64,{base64_pdf}#toolbar=1&navpanes=1&scrollbar=1&zoom=100" 
                        width="100%" 
                        height="100%" 
                        type="application/pdf"
                        style="border: none;"
                        allowfullscreen
                    >
                    </iframe>
                </div>
                """
                st.markdown(pdf_container, unsafe_allow_html=True)
            else:
                # 텍스트 보기
                st.text_area(
                    "추출된 원문 텍스트",
                    value=st.session_state.original_text,
                    height=600,
                    disabled=True
                )
            
        except Exception as e:
            st.error(f"PDF 처리 중 오류가 발생했습니다: {str(e)}")
    
    # 데이터베이스에서 불러온 번역 기록이 있지만 PDF가 없는 경우
    elif st.session_state.is_loading_from_db and not st.session_state.uploaded_file:
        st.info("이 번역 기록에는 PDF 파일이 저장되지 않았습니다.")
        st.text_area(
            "추출된 원문 텍스트",
            value=st.session_state.original_text,
            height=600,
            disabled=True
        )

with col2:
    st.subheader("🇰🇷 번역본")
    
    # 번역 버튼
    if st.session_state.pdf_uploaded and st.session_state.original_text:
        if st.button("🔄 번역 시작", type="primary", use_container_width=True):
            try:
                with st.spinner("번역 중... (시간이 다소 걸릴 수 있습니다)"):
                    translated_text = translate_text(st.session_state.original_text)
                    st.session_state.translated_text = translated_text
                    
                    # 번역 기록 저장
                    import re
                    import datetime
                    
                    # 마크다운에서 제목 추출 (첫 번째 # 제목)
                    title_match = re.search(r'^#\s+(.+)$', translated_text, re.MULTILINE)
                    if title_match:
                        title = title_match.group(1).strip()
                    else:
                        title = f"번역_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    
                    # PDF 바이트 데이터 준비 (업로드된 파일에서 직접 읽기)
                    pdf_bytes = None
                    if st.session_state.uploaded_file:
                        # 파일 포인터를 처음으로 이동
                        st.session_state.uploaded_file.seek(0)
                        pdf_bytes = st.session_state.uploaded_file.read()
                        st.session_state.uploaded_file.seek(0)  # 포인터 리셋
                        
                        # PDF 바이트 데이터 검증
                        if len(pdf_bytes) == 0:
                            st.warning("PDF 파일이 비어있습니다. 번역은 저장되지만 PDF는 저장되지 않습니다.")
                            pdf_bytes = None
                    
                    # 데이터베이스에 번역 기록 저장
                    translation_id = db.save_translation(
                        title=title,
                        original_text=st.session_state.original_text,
                        translated_text=translated_text,
                        pdf_bytes=pdf_bytes
                    )
                    
                    st.session_state.current_translation_id = translation_id
                
                st.success("번역 완료!")
                
            except Exception as e:
                st.error(f"번역 중 오류가 발생했습니다: {str(e)}")
    
    # 번역본 표시
    if st.session_state.translated_text:
        # 스크롤 가능한 마크다운 컨테이너 (PDF 뷰어와 동일한 높이)
        st.markdown("### 번역된 문서")
        
        # 스크롤 가능한 마크다운 뷰어 (PDF 뷰어와 정확히 같은 위치에서 시작)
        markdown_container = f"""
        <div style="
            height: 600px; 
            overflow-y: auto; 
            border: 1px solid #ddd; 
            border-radius: 5px;
            padding: 15px;
            background-color: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin-top: 60px;
        ">
            <div style="line-height: 1.6; color: #333333;">
                {st.session_state.translated_text}
            </div>
        </div>
        """
        st.markdown(markdown_container, unsafe_allow_html=True)
        
        # 다운로드 버튼
        st.markdown("---")
        st.subheader("📥 다운로드")
        
        # 번역본을 마크다운 형식으로 변환
        markdown_content = f"""# 번역된 논문

{st.session_state.translated_text}
"""
        
        st.download_button(
            label="📄 번역본 다운로드 (Markdown)",
            data=markdown_content,
            file_name="translated_paper.md",
            mime="text/markdown",
            use_container_width=True
        )
        
        # 원문과 번역본을 함께 다운로드
        combined_content = f"""# 원문 (Original)

{st.session_state.original_text}

---

# 번역본 (Translated)

{st.session_state.translated_text}
"""
        
        st.download_button(
            label="📄 원문+번역본 다운로드",
            data=combined_content,
            file_name="original_and_translated.md",
            mime="text/markdown",
            use_container_width=True
        )

# 사이드바에 사용법 안내 및 번역 기록
with st.sidebar:
    st.markdown("## 📋 사용법")
    st.markdown("""
    1. **PDF 업로드**: 왼쪽에 영어 논문 PDF를 드래그앤드롭
    2. **번역 시작**: 오른쪽의 '번역 시작' 버튼 클릭
    3. **결과 확인**: 번역된 한국어 텍스트 확인
    4. **다운로드**: 번역본을 Markdown 파일로 다운로드
    """)
    
    # 새 번역 생성 버튼
    st.markdown("## 🆕 새 번역")
    if st.button("📄 새 번역 생성", use_container_width=True, type="primary"):
        # 세션 상태 완전 초기화
        st.session_state.original_text = ""
        st.session_state.translated_text = ""
        st.session_state.pdf_uploaded = False
        st.session_state.uploaded_file = None
        st.session_state.current_translation_id = None
        st.session_state.is_loading_from_db = False
        
        # 삭제 확인 상태들도 초기화
        for key in list(st.session_state.keys()):
            if key.startswith("confirm_delete_"):
                del st.session_state[key]
        
        st.rerun()
    
    st.markdown("---")
    
    # 번역 기록 섹션
    st.markdown("## 📚 번역 기록")
    
    # 데이터베이스에서 번역 기록 불러오기
    translations = db.get_all_translations()
    
    if translations:
        for record in translations:
            # 현재 선택된 번역 기록인지 확인
            is_current = (st.session_state.current_translation_id == record['id'])
            
            # 번역 기록 컨테이너
            with st.container():
                col_title, col_delete = st.columns([4, 1])
                
                with col_title:
                    # 번역 기록 버튼
                    if st.button(
                        f"📄 {record['title'][:25]}{'...' if len(record['title']) > 25 else ''}",
                        key=f"history_{record['id']}",
                        use_container_width=True,
                        type="primary" if is_current else "secondary"
                    ):
                        # 선택된 번역 기록으로 복원
                        st.session_state.original_text = record['original_text']
                        st.session_state.translated_text = record['translated_text']
                        st.session_state.current_translation_id = record['id']
                        st.session_state.is_loading_from_db = True
                        
                        # PDF 파일 복원 (PDF 뷰어를 위해)
                        if record['pdf_data']:
                            import io
                            try:
                                pdf_bytes = base64.b64decode(record['pdf_data'])
                                # PDF 바이트 데이터 검증
                                if len(pdf_bytes) > 0:
                                    st.session_state.uploaded_file = io.BytesIO(pdf_bytes)
                                    st.session_state.pdf_uploaded = True
                                else:
                                    st.warning("저장된 PDF 파일이 손상되었습니다.")
                                    st.session_state.uploaded_file = None
                                    st.session_state.pdf_uploaded = False
                            except Exception as e:
                                st.error(f"PDF 파일 복원 중 오류가 발생했습니다: {str(e)}")
                                st.session_state.uploaded_file = None
                                st.session_state.pdf_uploaded = False
                        
                        st.rerun()
                
                with col_delete:
                    # 삭제 버튼
                    if st.button(
                        "🗑️",
                        key=f"delete_{record['id']}",
                        help="번역 기록 삭제",
                        type="secondary"
                    ):
                        # 삭제 확인
                        if st.session_state.get(f"confirm_delete_{record['id']}", False):
                            # 실제 삭제 실행
                            if db.delete_translation(record['id']):
                                st.success(f"'{record['title']}' 번역 기록이 삭제되었습니다.")
                                # 현재 선택된 기록이 삭제된 경우 상태 초기화
                                if st.session_state.current_translation_id == record['id']:
                                    st.session_state.original_text = ""
                                    st.session_state.translated_text = ""
                                    st.session_state.current_translation_id = None
                                    st.session_state.is_loading_from_db = False
                                    st.session_state.uploaded_file = None
                                    st.session_state.pdf_uploaded = False
                                st.rerun()
                            else:
                                st.error("번역 기록 삭제에 실패했습니다.")
                        else:
                            # 삭제 확인 상태 설정
                            st.session_state[f"confirm_delete_{record['id']}"] = True
                            st.rerun()
            
            # 생성 시간 표시
            st.caption(f"생성: {record['created_at']}")
            
            # 삭제 확인 메시지
            if st.session_state.get(f"confirm_delete_{record['id']}", False):
                st.warning(f"'{record['title']}' 번역 기록을 삭제하시겠습니까? 다시 삭제 버튼을 클릭하면 삭제됩니다.")
            
            st.markdown("---")
    else:
        st.info("아직 번역 기록이 없습니다.")
    
    st.markdown("## ⚠️ 주의사항")
    st.markdown("""
    - 구글 제미나이 API 키가 필요합니다
    - 번역은 전체 본문을 빠짐없이 수행합니다
    - 대용량 PDF의 경우 시간이 오래 걸릴 수 있습니다
    """)
    
    st.markdown("## 🔧 API 설정")
    st.markdown("""
    `.env` 파일에 다음을 추가하세요:
    ```
    GOOGLE_API_KEY=your_api_key_here
    ```
    """)

# 푸터
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit and Google Gemini AI")
