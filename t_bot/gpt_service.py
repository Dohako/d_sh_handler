import os
import openai

client = openai.OpenAI(api_key=os.getenv('GPT_API_KEY'))

async def send_text_to_gpt(text: str) -> str:
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": text,
                }
            ],
            model="gpt-3.5-turbo",
        )
        # Возвращаем первый ответ модели
        return response.choices[0].message.content
    except Exception as e:
        return f"Ошибка при взаимодействии с OpenAI API: {e}"
