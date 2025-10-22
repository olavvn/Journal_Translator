import sqlite3
import base64
import json
from datetime import datetime
from typing import List, Dict, Optional

class TranslationDatabase:
    def __init__(self, db_path: str = "translations.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """데이터베이스 테이블 초기화"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 번역 기록 테이블 생성
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS translations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                original_text TEXT,
                translated_text TEXT,
                pdf_data BLOB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_translation(self, title: str, original_text: str, translated_text: str, pdf_bytes: bytes = None) -> int:
        """번역 기록 저장"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO translations (title, original_text, translated_text, pdf_data, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, original_text, translated_text, pdf_bytes, datetime.now(), datetime.now()))
        
        translation_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return translation_id
    
    def get_all_translations(self) -> List[Dict]:
        """모든 번역 기록 조회"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, title, original_text, translated_text, pdf_data, created_at, updated_at
            FROM translations
            ORDER BY created_at DESC
        ''')
        
        columns = [description[0] for description in cursor.description]
        translations = []
        
        for row in cursor.fetchall():
            translation = dict(zip(columns, row))
            # PDF 데이터가 있으면 base64로 인코딩
            if translation['pdf_data']:
                translation['pdf_data'] = base64.b64encode(translation['pdf_data']).decode('utf-8')
            translations.append(translation)
        
        conn.close()
        return translations
    
    def get_translation_by_id(self, translation_id: int) -> Optional[Dict]:
        """특정 번역 기록 조회"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, title, original_text, translated_text, pdf_data, created_at, updated_at
            FROM translations
            WHERE id = ?
        ''', (translation_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            columns = ['id', 'title', 'original_text', 'translated_text', 'pdf_data', 'created_at', 'updated_at']
            translation = dict(zip(columns, row))
            # PDF 데이터가 있으면 base64로 인코딩
            if translation['pdf_data']:
                translation['pdf_data'] = base64.b64encode(translation['pdf_data']).decode('utf-8')
            return translation
        
        return None
    
    def delete_translation(self, translation_id: int) -> bool:
        """번역 기록 삭제"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM translations WHERE id = ?', (translation_id,))
        deleted_count = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        return deleted_count > 0
    
    def update_translation(self, translation_id: int, title: str = None, original_text: str = None, 
                         translated_text: str = None, pdf_bytes: bytes = None) -> bool:
        """번역 기록 업데이트"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 업데이트할 필드들
        update_fields = []
        values = []
        
        if title is not None:
            update_fields.append("title = ?")
            values.append(title)
        
        if original_text is not None:
            update_fields.append("original_text = ?")
            values.append(original_text)
        
        if translated_text is not None:
            update_fields.append("translated_text = ?")
            values.append(translated_text)
        
        if pdf_bytes is not None:
            update_fields.append("pdf_data = ?")
            values.append(pdf_bytes)
        
        if update_fields:
            update_fields.append("updated_at = ?")
            values.append(datetime.now())
            values.append(translation_id)
            
            query = f"UPDATE translations SET {', '.join(update_fields)} WHERE id = ?"
            cursor.execute(query, values)
            
            updated_count = cursor.rowcount
            conn.commit()
            conn.close()
            
            return updated_count > 0
        
        conn.close()
        return False
