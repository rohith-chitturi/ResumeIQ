import re
from typing import Dict, List

class SectionParser:
    """
    Parses a raw resume string into logical sections using heuristics.
    """
    
    SECTION_HEADERS = {
        "education": ["education", "academic background", "degrees"],
        "experience": ["experience", "work history", "employment", "professional experience"],
        "skills": ["skills", "technologies", "core competencies"],
        "projects": ["projects", "personal projects", "portfolio"],
    }
    
    @staticmethod
    def parse_sections(text: str) -> Dict[str, str]:
        """
        Splits resume text into sections based on known headers.
        """
        lines = text.split('\n')
        sections = {
            "education": "",
            "experience": "",
            "skills": "",
            "projects": "",
            "other": ""
        }
        
        current_section = "other"
        
        for line in lines:
            line_lower = line.strip().lower()
            
            # Check if this line is a header
            is_header = False
            for sec, headers in SectionParser.SECTION_HEADERS.items():
                if line_lower in headers or (len(line_lower) < 30 and any(h in line_lower for h in headers)):
                    current_section = sec
                    is_header = True
                    break
                    
            if not is_header and line.strip():
                sections[current_section] += line + "\n"
                
        return sections
