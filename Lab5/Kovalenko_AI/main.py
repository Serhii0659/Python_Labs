import io
import os
import platform
import sys
import time

from dotenv import load_dotenv
from google import genai

# Налаштування кодування для коректної роботи з кирилицею в терміналах WSL
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8", errors="replace")

PRICE_PER_1M_INPUT = 0.075
PRICE_PER_1M_OUTPUT = 0.30


def get_system_info():
    return {
        "os": f"{platform.system()} {platform.release()}",
        "kernel": platform.version(),
        "python": platform.python_version(),
    }


def calculate_usage_metrics(usage_metadata):
    input_tokens = usage_metadata.prompt_token_count
    output_tokens = usage_metadata.candidates_token_count
    total_tokens = usage_metadata.total_token_count

    cost_in = (input_tokens / 1000000) * PRICE_PER_1M_INPUT
    cost_out = (output_tokens / 1000000) * PRICE_PER_1M_OUTPUT
    total_cost = cost_in + cost_out

    return input_tokens, output_tokens, total_tokens, total_cost


def run_ai_query(client, model_id, prompt_text):
    max_retries = 3
    base_delay = 5

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model_id, contents=prompt_text
            )

            print("\n[Відповідь AI]:")
            print(response.text)

            in_t, out_t, total_t, cost = calculate_usage_metrics(
                response.usage_metadata
            )

            print("\n" + "=" * 50)
            print(f"Статистика виконання (Модель: {model_id}):")
            print(f"Кількість токенів на запит: {in_t}")
            print(f"Кількість токенів на відповідь: {out_t}")
            print(f"Загальна кількість: {total_t}")
            print(f"Загальна вартість операції: ${cost:.8f}")
            print("=" * 50 + "\n")
            return True

        except Exception as e:
            error_msg = str(e)
            if "503" in error_msg or "429" in error_msg:
                if attempt < max_retries - 1:
                    wait_time = base_delay * (2**attempt)
                    print(
                        f"\n[Сервер перевантажено. Спроба {attempt + 1}/{max_retries}]. Очікування {wait_time} секунд..."
                    )
                    time.sleep(wait_time)
                else:
                    print(
                        f"\n[Помилка]: API недоступний після {max_retries} спроб. Спробуй пізніше."
                    )
                    return False
            elif "404" in error_msg:
                return False
            else:
                print(f"\n[Непередбачена помилка API]: {e}")
                return False

    return False


def main():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print(
            "Критична помилка: GEMINI_API_KEY не знайдено в змінних середовища (.env)"
        )
        sys.exit(1)

    sys_info = get_system_info()
    print(f"Операційна система: {sys_info['os']}")
    print(f"Версія ядра/системи: {sys_info['kernel']}")
    print(f"Python: {sys_info['python']}\n")

    client = genai.Client(api_key=api_key)

    models = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-3-flash"]

    print("=== Інтерактивний режим Gemini AI ===")
    print("Введіть 'вихід' (або 'exit') для завершення роботи.\n")

    while True:
        try:
            user_prompt = input("Введіть ваш запит: ").strip()

            if user_prompt.lower() in ["вихід", "exit", "quit"]:
                print("\nЗавершення роботи. На все добре!")
                break

            if not user_prompt:
                continue

            success = False
            for m_id in models:
                if run_ai_query(client, m_id, user_prompt):
                    success = True
                    break

            if not success:
                print(
                    "\nКритична помилка: Не вдалося виконати запит за допомогою жодної з доступних моделей."
                )

        except KeyboardInterrupt:
            print("\n\nПроцес перервано користувачем (Ctrl+C). Вихід...")
            break
        except Exception as e:
            print(f"\nСталася неочікувана помилка у циклі: {e}")


if __name__ == "__main__":
    main()
