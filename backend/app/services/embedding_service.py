
from openai import AsyncOpenAI

from app.core.config import get_settings


class EmbeddingService:
    def __init__(self):
        settings = get_settings()

        self.client = AsyncOpenAI(
            api_key=settings.openai_api_key
        )

        self.model = "text-embedding-3-small"

    async def generate_embedding(self, text: str) -> list[float]:
        response = await self.client.embeddings.create(
            model=self.model,
            input=text,
        )

        return response.data[0].embedding
