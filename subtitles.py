import pysrt
import os

# Функція для завантаження субтитрів
def load_subtitles(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл {file_path} не знайдено!")
    return pysrt.open(file_path)

# Функція для паралельного виведення субтитрів
def print_parallel_subtitles(english_subs, ukrainian_subs):
    # Виведення субтитрів паралельно
    for eng_sub, ukr_sub in zip(english_subs, ukrainian_subs):
        print(f"Англійський: {eng_sub.text}")
        print(f"Український: {ukr_sub.text}")
        print("-" * 50)

# Шляхи до файлів
english_path = "/Users/macbook/Documents/диплом/скрипт/Never.Have.I.Ever.S01E10.720p.WEB.x264-GHOSTS.srt"
ukrainian_path = "/Users/macbook/Documents/диплом/скрипт/Never.Have.I.Ever.S01E10.WEBRip.Netflix.uk.srt"

try:
    english_subs = load_subtitles(english_path)
    ukrainian_subs = load_subtitles(ukrainian_path)

    print_parallel_subtitles(english_subs, ukrainian_subs)
except FileNotFoundError as e:
    print(e)
except Exception as e:
    print(f"Сталася помилка: {e}")