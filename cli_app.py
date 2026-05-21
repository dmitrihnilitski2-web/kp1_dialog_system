import os
from core.config_manager import config
from core.audio_engine import AudioEngine
from core.llm_engine import LLMEngine


def print_instructions():
    print("\n Інструкція користувача")
    print("1. Навігація та вихід:")
    print("   - У будь-який момент, щоб повернутися в меню,")
    print("     напишіть (або скажіть): 'назад', 'вихід' або 'стоп'.")
    print("\n2. Режим Echo-бот:")
    print("   - Бот просто повторює ваші слова.")
    print("   - Можна комбінувати текст та голос для вводу/виводу.")
    print("\n3. Режим Q&A (Питання-відповідь):")
    print("   - Відповідає на питання виключно за змістом файлу")
    print("     'data/context.txt'. Підтримує текст і голос.")
    print("\n4. Налаштування голосу:")
    print("   - Дозволяє обрати голос (українські/англійські),")
    print("     яким бот буде з вами розмовляти.\n")


def run_cli():
    audio = AudioEngine()
    llm = LLMEngine()

    print_instructions()

    while True:
        print("\n Головне меню (Діалогові програми)")
        print("0. Показати інструкцію")
        print("1. Echo-бот (з вибором формату вводу/виводу)")
        print("2. Q&A (відповіді за текстом з файлу)")
        print("3. Вибір голосу (Налаштування)")
        print("4. Вихід із застосунку\n")

        main_choice = input("Оберіть пункт меню (0-4): ").strip()

        if main_choice == '4':
            print("До побачення! Завершення роботи...")
            break

        elif main_choice == '0':
            print_instructions()

        elif main_choice == '3':
            while True:
                print("\n--- Доступні голоси ---")
                all_voices = audio.get_voices()
                available_voices = []

                for v in all_voices:
                    name_lower = v.name.lower()
                    id_lower = v.id.lower()
                    if "russian" in name_lower or "ru-ru" in id_lower or "ru_ru" in id_lower:
                        continue
                    available_voices.append(v)

                if not available_voices:
                    print("Не знайдено доступних голосів (крім відфільтрованих).")
                    break

                for i, v in enumerate(available_voices):
                    marker = "[v]" if config.voice_id == v.id else "[ ]"
                    print(f"{marker} [{i + 1}] {v.name}")

                print("\n[0] Повернутися в головне меню")
                voice_choice = input(f"Оберіть номер голосу (0-{len(available_voices)}): ").strip()

                if voice_choice == '0':
                    print("Повернення до головного меню...")
                    break

                if voice_choice.isdigit() and 1 <= int(voice_choice) <= len(available_voices):
                    selected_voice = available_voices[int(voice_choice) - 1]
                    config.voice_id = selected_voice.id
                    print(f"\nГолос успішно змінено на: {selected_voice.name}")
                    print("Тестуємо голос...")
                    audio.speak("Привіт! Тепер я розмовляю цим голосом.")
                else:
                    print("Невірний вибір. Спробуйте ще раз.")

        elif main_choice == '1':
            print("\n--- Формат роботи Echo-бота ---")
            print("1. Вводиш текст -> Отримуєш текст")
            print("2. Вводиш голосом -> Отримуєш голосом")
            print("3. Вводиш текст -> Отримуєш голосом")
            print("4. Вводиш голосом -> Отримуєш текст")

            echo_choice = input("Оберіть формат (1-4, або будь-що інше для відміни): ").strip()

            if echo_choice == '1':
                config.input_mode, config.output_mode = "Text", "Text"
            elif echo_choice == '2':
                config.input_mode, config.output_mode = "Voice", "Voice"
            elif echo_choice == '3':
                config.input_mode, config.output_mode = "Text", "Voice"
            elif echo_choice == '4':
                config.input_mode, config.output_mode = "Voice", "Text"
            else:
                print("Повернення до головного меню...")
                continue

            print("\n[Echo-бот запущено. Для виходу напишіть/скажіть 'назад']")

            while True:
                user_input = ""
                if config.input_mode == "Text":
                    user_input = input("\nВи: ")
                else:
                    user_input = audio.listen()
                    if user_input:
                        print(f"Ви (голос): {user_input}")

                if not user_input.strip():
                    continue

                if user_input.strip().lower() in ['вихід', 'назад', 'exit', 'стоп']:
                    print("Повертаємось до головного меню...")
                    break

                response = f"Echo: {user_input}"

                if config.output_mode == "Text":
                    print(f"Бот: {response}")
                else:
                    print(f"Бот: {response}")
                    audio.speak(response)

        elif main_choice == '2':
            context_path = os.path.join("data", "context.txt")
            if not os.path.exists(context_path):
                print(f"\nФайл {context_path} не знайдено! Створіть його та додайте текст.")
                continue

            with open(context_path, "r", encoding="utf-8") as f:
                qa_context = f.read()

            if not qa_context.strip():
                print(f"\nФайл {context_path} порожній! Додайте туди текст для аналізу.")
                continue

            print("\n--- Формат роботи Q&A ---")
            print("1. Вводиш текст -> Отримуєш текст")
            print("2. Вводиш голосом -> Отримуєш голосом")
            print("3. Вводиш текст -> Отримуєш голосом")
            print("4. Вводиш голосом -> Отримуєш текст")

            qa_choice = input("Оберіть формат (1-4, або будь-що інше для відміни): ").strip()

            if qa_choice == '1':
                config.input_mode, config.output_mode = "Text", "Text"
            elif qa_choice == '2':
                config.input_mode, config.output_mode = "Voice", "Voice"
            elif qa_choice == '3':
                config.input_mode, config.output_mode = "Text", "Voice"
            elif qa_choice == '4':
                config.input_mode, config.output_mode = "Voice", "Text"
            else:
                print("Повернення до головного меню...")
                continue

            print("\n[Режим Q&A запущено. Для виходу напишіть/скажіть 'назад']")

            while True:
                user_input = ""
                if config.input_mode == "Text":
                    user_input = input("\nВаше запитання до тексту (або 'назад'): ")
                else:
                    user_input = audio.listen()
                    if user_input:
                        print(f"Ви (голос): {user_input}")

                if not user_input.strip():
                    continue

                if user_input.strip().lower() in ['вихід', 'назад', 'exit', 'стоп']:
                    print("Повертаємось до головного меню...")
                    break

                print("Модель аналізує текст...")
                response = llm.generate_qa_response(user_input, qa_context)

                if config.output_mode == "Text":
                    print(f"\nВідповідь моделі:\n{response}")
                else:
                    print(f"\nВідповідь моделі:\n{response}")
                    audio.speak(response)

        else:
            print("Невірний вибір. Будь ласка, введіть число від 0 до 4.")
