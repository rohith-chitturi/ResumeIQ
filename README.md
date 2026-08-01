# ResumeIQ

ResumeIQ is an AI Retrieval Platform that analyzes resumes against job descriptions using semantic embeddings, deterministic ATS scoring, hybrid vector search, and LLM-powered recommendations. The platform combines explainable AI with a modular backend architecture to demonstrate modern AI engineering practices.

## System Architecture

```mermaid
graph TD
    A[Raw PDF] --> B(PDFParser)
    B --> C(SectionParser)
    C --> D(Skill Extraction)
    D --> E(ATSEngine)
    E --> F(Embedding Service)
    F --> G(Hybrid Ranking & pgvector)
    G --> H(Explainability Engine)
    H --> I(LLM Provider)
    I --> J{Structured JSON Dashboard}
```

## Concrete Capabilities

- **FastAPI Backend**: Asynchronous REST API managing the orchestration layer.
- **PostgreSQL + pgvector**: Stores resume embeddings and performs fast similarity searches.
- **Hybrid Semantic Retrieval**: Combines pgvector cosine distance (70%) with rule-based ATS scoring (30%).
- **Explainable ATS Scoring**: A deterministic Explainability Engine computes missing skills and match metrics natively.
- **Modular Provider Interfaces**: Swap between Gemini/OpenAI or SentenceTransformers/VoyageAI seamlessly.
- **Dependency Injection**: Centralized configuration and service injection for testability.
- **Repository Pattern**: Strict decoupling of business logic from SQLAlchemy ORM operations.
- **Dockerized Deployment**: Multi-container setup (Frontend, Backend, Database) managed via Docker Compose.
- **Continuous Integration**: Automated GitHub Actions running Ruff, MyPy, and Pytest.

## 📁 Repository Structure
```text
ResumeIQ/
├── backend/          # FastAPI REST API & SQLAlchemy Repositories
├── frontend/         # Streamlit Explainable Dashboard
├── shared/           # Domain models, Orchestrator, AI Services, DI
├── config/           # Pydantic Settings, Features, Dependencies
├── docs/             # Architecture Decision Records (ADRs)
├── scripts/          # CLI Tools (resumeiq analyze)
├── infra/            # Docker, docker-compose
└── .github/          # CI/CD Actions (Ruff, MyPy, Pytest)
```

## 🚀 Quick Start
```bash
# Clone the repository
git clone https://github.com/rohith-chitturi/ResumeIQ.git
cd ResumeIQ/infra

# Spin up the AI Platform
docker-compose up --build
```
- **Streamlit Dashboard**: `http://localhost:8501`
- **FastAPI Swagger API**: `http://localhost:8000/docs`

## 📊 API Endpoints
- `GET /health`
- `GET /metrics`
- `POST /api/v1/analyze` (End-to-End Analysis)
- `POST /api/v1/batch-analyze` (Async Batch Processing)

## 🗺 Technical Roadmap

To prevent feature creep and ensure a high-quality portfolio piece, ResumeIQ follows a strict versioned release schedule.

### ✅ v1.0: Production AI Platform (Current)
- FastAPI, Streamlit, Docker, PostgreSQL + pgvector
- Deterministic Explainability Engine & Hybrid Vector Search
- Repository Pattern & Dependency Injection

### 🚧 v2.0: AI Intelligence (Next)
- **Resume Tailoring**: Generate dynamically optimized resumes for specific target companies (Google, JPMC, etc.).
- **Multi-Job Optimization**: Rank one resume against 10 JDs simultaneously.
- **Interview Readiness**: Generate likely behavioral and technical questions based on identified resume gaps.
- **Recruiter Simulator**: Multi-perspective LLM critiques (ATS vs. Recruiter vs. Engineering Manager).

### 🔮 v3.0: Knowledge & RAG
- Integrate Retrieval-Augmented Generation (RAG) using curated HR knowledge bases, ATS best practices, and company-specific hiring guides.

### 🤖 v4.0: Agentic AI
- Transition from a linear pipeline to a multi-agent workflow (Manager Agent, Parser Agent, ATS Agent, Optimization Agent).

### 🏢 v5.0: Enterprise Recruitment Platform
- Auth (JWT/OAuth), Team/Organization management, and an HR candidate-tracking dashboard.
