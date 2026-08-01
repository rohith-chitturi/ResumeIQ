# ADR-002: Using pgvector for Vector Search

## Context
Resume matching requires dense vector retrieval. We could have used Pinecone, Milvus, or Qdrant. 

## Decision
We chose PostgreSQL with the `pgvector` extension. Since we already need relational storage for user profiles and analysis metadata, `pgvector` allows us to store the metadata and embeddings in the same table, eliminating data synchronization issues and reducing architectural complexity.

## Consequences
- **Pros:** ACID compliance, zero sync issues, simpler infrastructure (one less database to host).
- **Cons:** Scaling vector search in Postgres beyond tens of millions of rows requires careful indexing (HNSW/IVFFlat). For our current scale, it is optimal.
