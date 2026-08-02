# From Script to System: Architecting an AI Retrieval Platform

*By [Your Name]*

When building AI applications today, the default approach is incredibly tempting: take a user input, stuff it into an OpenAI prompt, and return the response. It’s fast, it’s easy, and it works perfectly—until you need to scale, evaluate, or debug it.

I recently built **ResumeIQ**, an AI-powered resume optimization platform. Very quickly, I realized that treating AI as a "black box script" was a massive architectural anti-pattern. 

Here is how I transformed ResumeIQ from a simple LLM wrapper into a mature, loosely-coupled **AI Systems Engineering Platform**.

## The Monolith Trap
In my v1.0, the core API looked something like this:
```python
def optimize_resume(resume_text, job_description):
    # 1. Parse text
    # 2. Call OpenAI with a massive prompt
    # 3. Return JSON
```
This worked, but it suffered from **Prompt Bloat**. The LLM was responsible for everything: extracting skills, understanding the company culture, and rewriting the text. As a result, the latency was high, and the hallucinations were frequent.

## Enter the Pipeline Architecture
To solve this, I decoupled the business logic from the LLM using a **Pipeline Engine**. 

Instead of one massive function, the data now flows through isolated `PipelineStage` objects via a single `PipelineContext`. 

```mermaid
graph LR
    Context --> ParseStage
    ParseStage --> ConstraintStage
    ConstraintStage --> RetrieveStage
    RetrieveStage --> LLMStage
```

### 1. Deterministic Fallbacks (The Constraint Stage)
Not everything needs an LLM. Before hitting the generative model, ResumeIQ uses a deterministic `ConstraintStage`. It performs a strict Gap Analysis between the candidate's parsed skills and the Job Description. By calculating the exact "Missing Skills" deterministically, we save tokens, reduce latency, and mathematically guarantee accuracy.

### 2. Hybrid Retrieval (Why pgvector?)
To match resumes to jobs at scale, semantic search (embeddings) isn't enough. If a job requires "Kubernetes", a semantic search might match "Docker"—which is semantically similar, but functionally incorrect for an ATS. 

By using **pgvector** inside PostgreSQL, ResumeIQ performs *Hybrid Retrieval*: combining the mathematical proximity of vector embeddings with the exact-match keyword querying of a relational database, all without the overhead of a dedicated vector database like Pinecone.

### 3. Production RAG (Retrieval-Augmented Generation)
To ensure the LLM rewrites the resume following actual industry standards, I implemented a generic RAG pipeline. 
The `RetrieveStage` chunks and indexes documents (like FAANG formatting guidelines). During execution, it retrieves the most relevant best-practices and injects them into the `PipelineContext`. The LLM is no longer guessing what a good resume looks like—it is explicitly citing our internal knowledge base.

## MLOps: Evaluating the Unpredictable
How do you know if your prompt actually improved? 
In v2.5, I implemented a lightweight **Experiment Tracker**. Every time the pipeline runs offline, it explicitly logs `metrics.json` (calculating `Recall@5` and `MRR`) to an `experiments/` directory. We can now explicitly prove whether switching from `MiniLM` to `BGE` embeddings actually improved retrieval performance on our ground-truth datasets.

## Conclusion
Building an AI application is easy. Building an AI *System* requires rigorous software engineering. 
By adopting a Pipeline Architecture, Deterministic Fallbacks, and MLOps Evaluation tracking, ResumeIQ became a scalable platform ready for enterprise use.

*Check out the source code and architecture diagrams on GitHub: [Link to Repo]*
