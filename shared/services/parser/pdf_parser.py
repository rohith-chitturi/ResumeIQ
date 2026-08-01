import fitz  # PyMuPDF
import re
import logging
from typing import Optional

# Setup basic logging for the module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PDFParser:
    """
    A robust class responsible for extracting and cleaning text from PDF resumes.
    Follows the Single Responsibility Principle (SRP) by doing only one thing: Parsing text.
    """
    
    @staticmethod
    def extract_text_from_bytes(pdf_bytes: bytes) -> Optional[str]:
        """
        Extracts text directly from an in-memory PDF byte stream.
        This is ideal for Streamlit web apps where users upload files without saving them to disk.
        
        Args:
            pdf_bytes (bytes): The byte stream of the uploaded PDF file.
            
        Returns:
            Optional[str]: The extracted and cleaned text, or None if an error occurs.
        """
        try:
            # PyMuPDF requires the stream and the filetype to read directly from memory
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            extracted_text = []
            
            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                # 'text' flag extracts raw text in reading order
                text = page.get_text("text")
                extracted_text.append(text)
                
            doc.close()
            
            # Combine all pages and clean the text
            full_text = "\n".join(extracted_text)
            return PDFParser._clean_text(full_text)
            
        except Exception as e:
            logging.error(f"Failed to parse PDF bytes: {e}")
            return None

    @staticmethod
    def _clean_text(text: str) -> str:
        """
        Cleans the extracted text by removing extraneous whitespaces and problematic characters.
        
        Args:
            text (str): The raw extracted text.
            
        Returns:
            str: The cleaned text.
        """
        if not text:
            return ""
            
        # Remove null bytes which can cause critical errors in LLMs and databases
        text = text.replace('\x00', ' ')
        
        # Replace 3 or more consecutive newlines with exactly two newlines
        # This keeps paragraph separation intact but prevents giant empty spaces
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Strip trailing and leading whitespace
        return text.strip()
