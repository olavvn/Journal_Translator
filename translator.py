import google.generativeai as genai
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 구글 제미나이 API 키
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def translate_text(text: str) -> str:
    """
    구글 제미나이 API를 사용하여 영어 텍스트를 한국어로 번역하는 함수
    
    Args:
        text: 번역할 영어 텍스트
        
    Returns:
        str: 번역된 한국어 텍스트
    """
    try:
        # 구글 제미나이 API 설정
        genai.configure(api_key=GOOGLE_API_KEY)
        
        # 모델 초기화
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # 번역 프롬프트
        prompt = f"""
        다음 영어 논문을 한국어로 번역해주세요. 
        번역 시 다음 사항을 준수해주세요:
        1. 학술 논문의 정확성과 전문성을 유지
        2. 모든 내용을 빠짐없이 번역 (생략하지 말 것)
        3. 자연스러운 한국어로 번역. 문장 구조를 유지하며 번역하고, "-해라"체 형식으로 번역할 것 (예: "This is a test" -> "이것은 테스트이다.")
        4. 전문 용어는 적절히 번역하되 필요시 원문을 병기
        5. 논문의 구조와 형식을 유지
        6. 마크다운 형식으로 출력 (제목은 #, ##, ### 사용, 목록은 -, 번호는 1. 사용)
        7. 수식이 있다면 LaTeX 형식으로 유지
        8. 표와 그림 설명도 번역
        9. 번역 작업만 수행하고, 번역문 앞뒤에 지시사항을 수행했다는 문구를 추가하지 말 것 (예: "번역 작업을 완료했습니다.")
        
        영어 원문:
        {text}
        """
        
        # 번역 실행
        response = model.generate_content(prompt)
        
        return response.text
    
    except Exception as e:
        raise Exception(f"번역 중 오류가 발생했습니다: {str(e)}")
