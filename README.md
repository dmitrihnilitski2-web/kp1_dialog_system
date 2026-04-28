kp1_dialog_system/
│
├── core/                       # Ядро бізнес-логіки
│   ├── __init__.py
│   ├── config_manager.py       # Управління станом і налаштуваннями
│   ├── audio_engine.py         # STT та TTS (SpeechRecognition, pyttsx3)
│   └── llm_engine.py           # Робота з Google GenAI SDK (чати та Q&A)
│
├── interfaces/                 # Інтерфейси користувача
│   ├── __init__.py
│   ├── cli_app.py              # Консольний застосунок (Echo та Команди)
│   └── web_app.py              # Streamlit застосунок (усі модулі)
│
├── data/                       # Локальні дані
│   └── context.txt             # Текстовий файл для завдання Q&A з контекстом
│
├── requirements.txt            # Залежності проекту
└── main.py                     # Точка входу (маршрутизатор для запуску CLI або Web)
