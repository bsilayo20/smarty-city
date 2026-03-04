import redis
from openai import OpenAI
from app.core.config import settings

redis_client = redis.from_url(settings.REDIS_URL)
client = OpenAI(api_key=settings.OPENAI_API_KEY)

async def generate_ai_response(prompt: str):
    cached = redis_client.get(prompt)
    if cached:
        return cached.decode()

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        result = response.choices[0].message.content
        redis_client.set(prompt, result, ex=3600)
        return result
    except Exception as e:
        return f"AI Error: {str(e)}"
