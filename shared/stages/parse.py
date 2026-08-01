from typing import Optional
from shared.pipeline.engine import PipelineStage
from shared.pipeline.context import PipelineContext
from shared.services.parser.section_parser import SectionParser


class ParseStage(PipelineStage):
    """
    Parses raw resume text into structured sections.
    """
    def __init__(self, parser: Optional[SectionParser] = None):
        # Allow dependency injection or default initialization
        self.parser = parser or SectionParser()

    async def execute(self, context: PipelineContext) -> None:
        if not context.resume_text:
            context.fail_validation("ParseStage failed: No resume_text provided in context.")
            return

        try:
            # Execute parsing
            sections = self.parser.extract_sections(context.resume_text)
            
            # Update context
            context.parsed_sections = sections
            
            # Record metrics
            context.add_metric("parse_section_count", len(sections))
            
        except Exception as e:
            context.fail_validation(f"ParseStage failed: {str(e)}")
