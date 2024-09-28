import os
import cohere

co = cohere.ClientV2(os.getenv('COHERE_API_KEY'))


async def send_text_to_cohere(text: str) -> str:
    try:
        response = co.chat(
            model="command-r-plus",
            messages=[
                {
                    "role": "user",
                    "content": text
                }
            ]
        )
        # Возвращаем первый ответ модели
        return response.message.content[0].text
    except Exception as e:
        return f"Ошибка при взаимодействии с COHERE API: {e}"