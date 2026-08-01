from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.repositories.base import BaseRepository
from backend.db.models import ResumeAnalysis

class ResumeRepository(BaseRepository[ResumeAnalysis]):
    
    async def search_by_jd(self, db: AsyncSession, jd_vector: list, limit: int = 10):
        """
        Uses pgvector to perform a cosine distance search (<=>)
        """
        # Order by cosine distance and limit results
        stmt = select(self.model).order_by(self.model.embedding.cosine_distance(jd_vector)).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()
