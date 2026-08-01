from shared.pipeline.engine import PipelineStage
from shared.pipeline.context import PipelineContext
from shared.rag.retriever import Retriever


class RetrieveStage(PipelineStage):
    """
    RAG Stage: Queries the VectorStore to retrieve domain knowledge and best practices.
    Injects the retrieved documents into the context before LLM generation.
    """
    def __init__(self, retriever: Retriever):
        self.retriever = retriever

    async def execute(self, context: PipelineContext) -> None:
        try:
            # We use the constraints/missing skills to drive the retrieval query
            # If no constraints, we use the company profile keywords
            if context.constraints:
                query = " ".join(context.constraints)
            elif context.company_profile:
                query = " ".join(context.company_profile.get("keywords", []))
            else:
                query = "general resume best practices"
                
            knowledge = self.retriever.retrieve_context(query)
            
            context.retrieved_knowledge = knowledge
            context.add_metric("retrieved_knowledge_length", len(knowledge))
            
        except Exception as e:
            context.fail_validation(f"RetrieveStage failed: {str(e)}")
