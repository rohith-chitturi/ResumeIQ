# ADR-001: Repository Pattern

## Context
As ResumeIQ grows, tying the business logic directly to SQLAlchemy ORM queries makes the code brittle, difficult to test, and hard to migrate if we ever change databases.

## Decision
We implemented the Repository Pattern in `backend/repositories/`. All database access is abstracted behind generic and specific repository classes (e.g., `ResumeRepository`). The services interact only with the repository interfaces, never with the ORM directly.

## Consequences
- **Pros:** Highly testable (we can mock the repository), decoupled business logic, easier migration paths.
- **Cons:** Slight boilerplate overhead for simple queries.
