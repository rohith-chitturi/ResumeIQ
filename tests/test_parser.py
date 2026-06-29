import pytest
import fitz
from parser.pdf_parser import PDFParser

def generate_dummy_pdf_bytes(text_content: str) -> bytes:
    """Helper function to create an in-memory PDF for testing."""
    doc = fitz.open()
    page = doc.new_page()
    # Insert text at coordinates (50, 50)
    page.insert_text((50, 50), text_content)
    pdf_bytes = doc.write()
    doc.close()
    return pdf_bytes

def test_extract_text_valid_pdf():
    # Arrange
    raw_text = "John Doe\nSoftware Engineer\nPython, AI"
    pdf_bytes = generate_dummy_pdf_bytes(raw_text)
    
    # Act
    extracted_text = PDFParser.extract_text_from_bytes(pdf_bytes)
    
    # Assert
    assert extracted_text is not None
    assert "John Doe" in extracted_text
    assert "Software Engineer" in extracted_text

def test_clean_text_removes_null_bytes():
    # Arrange
    dirty_text = "Hello\x00World"
    
    # Act
    cleaned_text = PDFParser._clean_text(dirty_text)
    
    # Assert
    assert "\x00" not in cleaned_text
    assert cleaned_text == "Hello World"

def test_clean_text_reduces_newlines():
    # Arrange
    dirty_text = "Line 1\n\n\n\nLine 2"
    
    # Act
    cleaned_text = PDFParser._clean_text(dirty_text)
    
    # Assert
    assert "\n\n\n" not in cleaned_text
    assert cleaned_text == "Line 1\n\nLine 2"

def test_extract_text_invalid_bytes():
    # Arrange
    invalid_bytes = b"not a real pdf"
    
    # Act
    extracted_text = PDFParser.extract_text_from_bytes(invalid_bytes)
    
    # Assert
    assert extracted_text is None
