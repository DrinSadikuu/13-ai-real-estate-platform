
from openai import OpenAI
from app.core.config import get_settings
import numpy as np

settings = get_settings()
client = OpenAI(api_key=settings.openai_api_key)

texts = [
    "I want a quiet apartment near a park",
    "A peaceful flat close to green spaces",
    "A busy commercial office in the city center",
]

response = client.embeddings.create(
    model="text-embedding-3-small",
    input=texts,
)

embeddings = [
    item.embedding for item in response.data
]

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )

print("Query:", texts[0])

for i in range(1, len(texts)):
    score = cosine_similarity(
        embeddings[0],
        embeddings[i],
    )

    print(f"{texts[i]}: {score:.4f}")
