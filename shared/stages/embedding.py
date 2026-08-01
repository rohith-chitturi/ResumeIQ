from typing import Optional
from shared.pipeline.engine import PipelineStage
from shared.pipeline.context import PipelineContext
from shared.embeddings.base import EmbeddingProvider


class EmbeddingStage(PipelineStage):
    """
    Converts parsed resume sections into vector embeddings.
    """
    def __init__(self, provider: EmbeddingProvider):
        self.provider = provider

    async def execute(self, context: PipelineContext) -> None:
        if not context.parsed_sections:
            context.fail_validation("EmbeddingStage skipped: No parsed sections available.")
            return

        try:
            embeddings = {}
            for section_name, text in context.parsed_sections.items():
                if text.strip():
                    vector = self.provider.generate_embedding(text)
                    embeddings[section_name] = vector
            
            context.embeddings = embeddings
            context.add_metric("embedded_sections_count", len(embeddings))
            
        except Exception as e:
            context.fail_validation(f"EmbeddingStage failed: {str(e)}")
