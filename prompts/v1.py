class PromptManager:
    """
    Version 1 Prompts for ResumeIQ.
    """

    @staticmethod
    def get_ats_analysis_prompt(resume_text: str, job_description: str) -> str:
        return f"""
        You are an expert ATS (Applicant Tracking System) Analyzer and Senior Tech Recruiter.
        Your goal is to evaluate a candidate's resume against a specific job description.

        Job Description:
        ---
        {job_description}
        ---

        Candidate's Resume:
        ---
        {resume_text}
        ---

        Perform a deep analysis and provide constructive feedback. 
        Focus strictly on extracting the missing hard skills and providing actionable bullet point improvements.
        Return the result strictly as a structured JSON object matching the requested schema.
        """
