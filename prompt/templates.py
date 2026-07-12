class PromptManager:
    """
    Manages all prompt templates used for interacting with the LLM.
    
    Why separate this?
    - Prompt Engineering is an iterative process. Mixing giant strings inside `app.py` or `services.py` 
      makes the code unreadable and hard to maintain.
    - Centralizing prompts allows us to easily tweak instructions without touching business logic.
    """

    @staticmethod
    def get_ats_analysis_prompt(resume_text: str, job_description: str) -> str:
        """
        Constructs the main instruction prompt for Gemini to analyze the resume against the JD.
        
        Args:
            resume_text (str): The parsed text from the PDF.
            job_description (str): The target job description.
            
        Returns:
            str: The fully formatted prompt ready to be sent to the LLM.
        """
        return f"""
        You are an expert ATS (Applicant Tracking System) Analyzer and Senior Tech Recruiter.
        Your goal is to evaluate a candidate's resume against a specific job description.

        Here is the Job Description:
        ---
        {job_description}
        ---

        Here is the Candidate's Resume:
        ---
        {resume_text}
        ---

        Perform a deep analysis and provide constructive feedback. 
        Focus strictly on extracting the missing hard skills and providing actionable bullet point improvements.
        Do not flatter the candidate; be highly critical and professional.
        """
