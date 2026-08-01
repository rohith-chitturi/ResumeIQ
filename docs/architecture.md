# Architecture Overview

ResumeIQ is built using a modern AI Engineering Service Layer pattern.

## Core Components
1. **Frontend (Streamlit)**: Provides the Explainable AI Dashboard, visualizing vector similarity and LLM feedback.
2. **Backend (FastAPI)**: Serves the RESTful endpoints.
3. **AI Orchestrator**: Manages the flow of data through the AI services.
4. **Vector Database (PostgreSQL + pgvector)**: Stores Resume and JD embeddings for future similarity search.

## The Pipeline
`PDF -> Section Parser -> ATS Engine (Cosine Similarity on Embeddings) -> Prompt Builder -> Gemini LLM -> Structured JSON`

## Services
- `EmbeddingService`: Converts text into `all-MiniLM-L6-v2` dense vectors. Uses LRU caching to save compute on identical strings.
- `ATSEngine`: Breaks the resume into logical sections and calculates sub-scores for explainability.
- `GeminiService`: Handles communication with Google GenAI SDK, wrapped in `tenacity` for automatic retry on rate limits.
