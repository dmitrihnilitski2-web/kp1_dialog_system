import os
from google import genai
from dotenv import load_dotenv

load_dotenv()  


class LLMEngine:
    def __init__(self):
        try:
            self.client = genai.Client()
            self.chat_session = self.client.chats.create(model='gemini-2.5-flash')
        except Exception as e:
            print(f"Помилка ініціалізації GenAI: {e}")
            self.client = None
            self.chat_session = None

    def generate_chat_response(self, prompt: str) -> str:
        """Вільний діалог з мовною моделлю."""
        if not self.chat_session:
            return "Помилка: Модель не ініціалізована. Перевірте GOOGLE_API_KEY."

        response = self.chat_session.send_message(prompt)
        return response.text

    def generate_qa_response(self, prompt: str, context: str) -> str:
        """Відповідь на питання строго за наданим контекстом."""
        if not self.client:
            return "Помилка: Модель не ініціалізована."

        full_prompt = f"""
        Ти корисний асистент. Дай відповідь на питання, спираючись виключно на наданий контекст. 
        Якщо в контексті немає відповіді, скажи "Я не знаю".

        Контекст:
        {context}

        Питання:
        {prompt}
        """
        response = self.client.models.generate_content(
            model='gemini-2.5-flash',
            contents=full_prompt
        )
        return response.text