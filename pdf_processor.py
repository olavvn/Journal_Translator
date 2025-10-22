import PyPDF2
import io

def extract_text_from_pdf(pdf_file) -> str:
    """
    PDF 파일에서 텍스트를 추출하는 함수
    
    Args:
        pdf_file: 업로드된 PDF 파일 객체
        
    Returns:
        str: 추출된 텍스트
    """
    try:
        # PDF 파일 읽기
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        
        # 모든 페이지의 텍스트 추출
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text() + "\n"
        
        return text.strip()
    
    except Exception as e:
        raise Exception(f"PDF 텍스트 추출 중 오류가 발생했습니다: {str(e)}")
