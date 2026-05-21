import pyttsx3
import speech_recognition as sr
from core.config_manager import config


class AudioEngine:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def get_voices(self):
        """Повертає список доступних голосів (включаючи RHVoice)."""
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        return voices

    def speak(self, text: str):
        """Озвучує текст з урахуванням поточних налаштувань."""
        engine = pyttsx3.init()

        engine.setProperty('volume', config.volume)
        engine.setProperty('rate', config.rate)
        if config.voice_id:
            engine.setProperty('voice', config.voice_id)

        engine.say(text)
        engine.runAndWait()
        engine.stop()  

    def listen(self, timeout_sec=5, phrase_limit_sec=15) -> str:
        """Слухає мікрофон з таймаутом та повертає розпізнаний текст."""
        with sr.Microphone() as source:
            print(f"Слухаю... (мовчіть {timeout_sec} сек для відміни)")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)

            try:
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout_sec,
                    phrase_time_limit=phrase_limit_sec
                )
            except sr.WaitTimeoutError:
                return ""

        try:
            text = self.recognizer.recognize_google(audio, language="uk-UA")
            return text
        except sr.UnknownValueError:
            return ""  
        except sr.RequestError as e:
            return f"[Помилка сервісу розпізнавання: {e}]"