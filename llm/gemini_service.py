import os
import logging
from typing import Optional
from google import genai
from google.genai import types
from pydantic import ValidationError

from models.schemas import ATSFeedbackResponse
from prompt.templates import PromptManager

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GeminiService:
    """
    A service class dedicated to interacting with the Gemini LLM via the official `google-genai` SDK.
    
    Why this architecture?
    - Encapsulation: We hide the complexity of the Google GenAI SDK behind a simple method.
    - If we ever want to switch to a different LLM (like Claude or GPT-4), we only need to rewrite this class.
      The rest of the app (`app.py`) stays completely identical.
    """

    def __init__(self):
        """
        Initializes the Gemini client using the API key from the environment.
        """
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "your_gemini_api_key_here":
            logging.error("GEMINI_API_KEY is missing or invalid in environment.")
            self.client = None
        else:
            # We use the new google-genai client
            self.client = genai.Client(api_key=api_key)
            logging.info("Gemini Client initialized.")

    def analyze_resume(self, resume_text: str, job_description: str) -> Optional[ATSFeedbackResponse]:
        """
        Sends the resume and job description to Gemini and requests a structured JSON response.
        
        Args:
            resume_text (str): The extracted text from the PDF.
            job_description (str): The target Job Description.
            
        Returns:
            Optional[ATSFeedbackResponse]: A validated Pydantic object containing the feedback, or None if an error occurs.
        """
        if not self.client:
            logging.error("Cannot analyze resume: Gemini Client is not initialized.")
            return None
            
        prompt = PromptManager.get_ats_analysis_prompt(resume_text, job_description)
        
        try:
            # We use gemini-2.5-flash as it is fast and excellent at reasoning tasks
            # We pass our Pydantic schema to response_schema to enforce structured output.
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=ATSFeedbackResponse,
                    temperature=0.2, # Low temperature because we want analytical, deterministic feedback
                ),
            )
            
            # The SDK automatically handles the JSON parsing and validation against our Pydantic model
            # response.parsed is an instance of ATSFeedbackResponse
            if response.parsed:
                return response.parsed
            else:
                logging.error("Response was generated but could not be parsed into the schema.")
                return None
                
        except Exception as e:
            logging.error(f"Error calling Gemini API: {e}")
            return None
