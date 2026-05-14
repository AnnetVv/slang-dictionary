import json
import csv

# Шлях до CSV файлу
csv_path = '/Users/macbook/Documents/диплом/Словник.csv'
# Шлях до CSV-файлу зі словником
data_list = []

# Сфери сленгу
allowed_spheres = [
    'Стосунки між людьми (повсякденні взаємини між людьми)',
    'Стосунки між людьми (романтичні та сексуальні взаємини)',
    'Фізична діяльність',
    'Захоплення',
    'Людина та навколишній світ (їжа)',
    'Людина та навколишній світ (настрій)',
    'Людина та навколишній світ (одяг)',
    'Людина та навколишній світ (характеристика людини)',
    'Людина та навколишній світ (гроші)',
    'Людина та навколишній світ (частини людського тіла)',
    'Людина та навколишній світ (емоції)',
    'Людина та навколишній світ (наркотики)',
    'Людина та навколишній світ (навчання)'
]

# Типи емоційного забарвлення
allowed_emotions = ['Нейтральне', 'Грубе', 'Жартівливе', 'Іронічне', 'Глузливе', 'Зверхнє', 'Зневажливе', 'Вульгарне']


# Функція очищення тексту
def clean_text(text):
    if not text:
        return ''
    text = str(text).strip()
    if text.startswith('"') and text.endswith('"'):
        text = text[1:-1]
    return text


# Робить першу літеру великою
def capitalize_first(text):
    if not text:
        return ''
    return text[0].upper() + text[1:] if len(text) > 1 else text.upper()


# Читання CSV
with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=';')
    headers = next(reader)
    rows = list(reader)


# Робить першу літеру великою
def split_contexts(text):
    if not text:
        return []
    text = text.replace('\\n', '\n').replace('\u2028', '\n').replace('\r\n', '\n').replace('\r', '\n')
    # Функція для розділення контекстів
    parts = [p.strip() for p in text.split('\n') if p.strip()]
    return parts


# Обробка кожного рядка таблиці
for row_num, row in enumerate(rows, start=2):
    # Якщо рядок неповний — пропускаємо
    if len(row) < 5:
        continue

    # Основні контексти
    main_context_en = clean_text(row[5]) if len(row) > 5 else ''
    main_context_ua = clean_text(row[6]) if len(row) > 6 else ''
    # Основні контексти
    alternatives = clean_text(row[7]) if len(row) > 7 else ''
    # Контексти альтернатив
    alt_context_en = clean_text(row[8]) if len(row) > 8 else ''
    alt_context_ua = clean_text(row[9]) if len(row) > 9 else ''
    # Основні дані слова
    english = clean_text(row[0])
    ukrainian = clean_text(row[1])
    meaning = clean_text(row[2])
    sphere = clean_text(row[3]).strip()
    emotion = clean_text(row[4]).strip()
    # Фільтрація сфер
    if sphere not in allowed_spheres:
        continue
    # Фільтрація емоцій
    if emotion not in allowed_emotions:
        continue

    # Список альтернативних перекладів
    alternatives_list = []
    # Перевірка чи є альтернативи
    has_alternatives = False

    # Якщо існують альтернативні переклади
    if alternatives:
        # Розділяємо альтернативи через кому
        alt_parts = [a.strip() for a in alternatives.split(',') if a.strip()]
        # Розділяємо контексти
        alt_contexts_en = split_contexts(alt_context_en)
        alt_contexts_ua = split_contexts(alt_context_ua)
        # Обробка кожної альтернативи
        for i, alt in enumerate(alt_parts):
            # Робимо першу літеру великою
            alt_capitalized = capitalize_first(alt)

            # Якщо є обидва контексти
            if i < len(alt_contexts_en) and i < len(alt_contexts_ua):
                alternatives_list.append({
                    'alternative': alt_capitalized,
                    'context_en': alt_contexts_en[i],
                    'context_ua': alt_contexts_ua[i]
                })
            else:
                alternatives_list.append({
                    'alternative': alt_capitalized,
                    'context_en': '',
                    'context_ua': ''
                })

        # Якщо список не порожній
        has_alternatives = len(alternatives_list) > 0

    # Замінюємо переноси рядків
    main_context_en_display = main_context_en.replace('\\n', '<br>').replace('\u2028', '<br>').replace('\n', '<br>')
    main_context_ua_display = main_context_ua.replace('\\n', '<br>').replace('\u2028', '<br>').replace('\n', '<br>')
    # Створення словника для слова
    word = {
        'english': english,
        'ukrainian': ukrainian,
        'meaning': meaning,
        'sphere': sphere,
        'emotion': emotion,
        'context_en': main_context_en_display,
        'context_ua': main_context_ua_display,
        'has_alternatives': has_alternatives,
        'alternatives_list': alternatives_list
    }

    data_list.append(word)

print(f"Завантажено {len(data_list)} слів")
# Пошук слів з альтернативними перекладами
words_with_alt = [w for w in data_list if w['has_alternatives']]
print(f"Слів з альтернативними перекладами: {len(words_with_alt)}")
# Формування списків сфер та емоцій
spheres_list = sorted(list(set([w['sphere'] for w in data_list if w['sphere']])))
emotions_list = sorted(list(set([w['emotion'] for w in data_list if w['emotion']])))

# Створення HTML
html_content = f'''<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
    <title>Словник молодіжного сленгу</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        html {{
            height: 100%;
            overflow-y: auto;
        }}

        input, select, textarea, button {{
            -webkit-tap-highlight-color: transparent;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100%;
            overflow-y: auto;
            -webkit-overflow-scrolling: touch;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
            display: flex;
            flex-direction: column;
            height: 90vh;
            position: relative;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            text-align: center;
            flex-shrink: 0;
            position: relative;
        }}
        .header h1 {{ font-size: 2em; }}

        .info-circle {{
            position: absolute;
            top: 20px;
            right: 20px;
            width: 40px;
            height: 40px;
            background-color: white;
            color: #667eea;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            z-index: 100;
        }}
        .info-circle:hover {{
            transform: scale(1.05);
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }}

        .filters {{
            padding: 15px 20px;
            background: #f8f9fa;
            border-bottom: 2px solid #e0e0e0;
            flex-shrink: 0;
        }}
        .filter-group {{
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }}
        .filter-item {{
            flex: 1;
            min-width: 200px;
            position: relative;
            overflow: visible;
        }}
        .filter-item label {{
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }}
        .filter-item select,
        .filter-item input {{
            width: 100%;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px; 

            outline: none !important;
            box-shadow: none !important;

            appearance: none;
            -webkit-appearance: none;
        }}
        .filter-item input:focus,
        .filter-item select:focus {{
            outline: none !important;
            box-shadow: none !important;
            border-color: #667eea;
        }}
        .filter-item input {{
            font-size: 16px; 
        }}
        .button-group {{
            display: flex;
            gap: 10px;
            margin-top: 15px;
        }}
        button {{
            padding: 8px 16px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
        }}
        button:hover {{ background: #764ba2; }}
        .clear-btn {{ background: #dc3545; }}

        .result-counter {{
            margin-top: 12px;
            padding: 8px 12px;
            background: #e8eaf6;
            border-radius: 8px;
            font-size: 14px;
            color: #667eea;
            font-weight: bold;
            text-align: center;
        }}

        .table-container {{
            padding: 15px 20px;
            flex: 1;
            overflow-x: auto;
            overflow-y: auto;
            -webkit-overflow-scrolling: touch;
            position: relative;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            min-width: 700px;
        }}
        th {{
            background: #667eea;
            color: white;
            padding: 12px;
            text-align: left;
            position: sticky;
            top: 0;
            z-index: 10;
        }}
        td {{
            padding: 10px 12px;
            border-bottom: 1px solid #ddd;
            vertical-align: top;
        }}
        tr:hover {{ background: #f5f5f5; }}
        .clickable-word {{
            color: #667eea;
            cursor: pointer;
            text-decoration: underline;
        }}
        .clickable-word:hover {{ color: #764ba2; }}
        .modal {{
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            overflow-y: auto;
            -webkit-overflow-scrolling: touch;
        }}
        .modal-content {{
            background: white;
            margin: 5% auto;
            padding: 25px;
            border-radius: 15px;
            width: 70%;
            max-width: 750px;
            max-height: 85vh;
            overflow-y: auto;
            position: relative;
            -webkit-overflow-scrolling: touch;
        }}
        .close {{
            position: absolute;
            right: 20px;
            top: 15px;
            font-size: 28px;
            cursor: pointer;
        }}
        .alternative-item {{
            background: #f8f9fa;
            padding: 12px;
            border-radius: 8px;
            margin: 12px 0;
            border-left: 4px solid #667eea;
        }}
        .alternative-word {{
            font-weight: bold;
            color: #667eea;
            font-size: 16px;
            margin-bottom: 8px;
        }}
        .context-text {{
            margin-top: 5px;
            padding-left: 15px;
            color: #555;
        }}
        .context-en, .context-ua {{
            font-style: italic;
            margin-bottom: 5px;
        }}
        .autocomplete-items {{
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background-color: white;
            border: 2px solid #667eea;
            border-top: none;
            border-radius: 0 0 8px 8px;
            max-height: 300px;
            overflow-y: auto;
            z-index: 99;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            display: none;
            -webkit-overflow-scrolling: touch;
        }}
        .autocomplete-items:empty {{
            display: none;
            border: none;
            box-shadow: none;
        }}
        .autocomplete-item {{
            padding: 12px 15px;
            cursor: pointer;
            border-bottom: 1px solid #eee;
            font-size: 15px;
        }}
        .autocomplete-item:hover {{
            background-color: #f0f0f0;
        }}
        .autocomplete-no-result {{
            padding: 12px 15px;
            color: #999;
            text-align: center;
            font-size: 14px;
        }}
        hr {{ margin: 15px 0; border: none; border-top: 1px solid #ddd; }}

        @media (max-width: 768px) {{
            input, select, textarea {{
                font-size: 16px !important;
            }}

            html, body {{
                height: auto;
                overflow-y: auto;
                -webkit-overflow-scrolling: touch;
                touch-action: pan-y;
            }}
            body {{
                padding: 10px;
            }}
            .container {{
                height: auto;
                min-height: 95vh;
                overflow: visible;
            }}
            .header h1 {{
                font-size: 1.3em;
            }}
            .header p {{
                font-size: 0.9em;
            }}
            .info-circle {{
                width: 30px;
                height: 30px;
                font-size: 16px;
                top: 12px;
                right: 12px;
            }}
            .filter-group {{
                flex-direction: column;
                gap: 10px;
            }}
            .filter-item {{
                min-width: 100%;
            }}
            .table-container {{
                flex: none;
                max-height: 60vh;
                overflow-y: auto;
                overflow-x: auto;
                -webkit-overflow-scrolling: touch;
                touch-action: pan-x pan-y;
            }}
            .modal-content {{
                width: 95%;
                margin: 10% auto;
                padding: 15px;
                max-height: 80vh;
            }}
            th, td {{
                padding: 8px;
                font-size: 12px;
            }}
            .button-group button {{
                padding: 10px;
                font-size: 14px;
            }}
        }}

        @media (max-width: 480px) {{
            th, td {{
                padding: 6px;
                font-size: 11px;
            }}
            .filter-item select,
            .filter-item input {{
                padding: 8px;
                font-size: 16px !important; 
            }}
            .table-container {{
                padding: 10px;
                max-height: 55vh;
            }}
        }}
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>Словник молодіжного сленгу</h1>
        <p>Англійський та український молодіжний сленг</p>
        <div class="info-circle" onclick="openInfoModal()">ℹ️</div>
    </div>
    <div class="filters">
        <div class="filter-group">
            <div class="filter-item">
                <label>📚 Сфера:</label>
                <select id="sphereFilter" onchange="filterTable()">
                    <option value="">Всі сфери</option>
                    {''.join([f'<option value="{s}">{s}</option>' for s in spheres_list])}
                </select>
            </div>
            <div class="filter-item">
                <label>🎭 Емоційне забарвлення:</label>
                <select id="emotionFilter" onchange="filterTable()">
                    <option value="">Всі емоції</option>
                    {''.join([f'<option value="{e}">{e}</option>' for e in emotions_list])}
                </select>
            </div>
            <div class="filter-item">
                <label>🔍 Пошук:</label>
                <input type="text" id="searchInput" placeholder="Введіть слово..." autocomplete="off">
                <div id="autocompleteList" class="autocomplete-items"></div>
            </div>
        </div>
        <div class="button-group">
            <button class="clear-btn" onclick="clearFilters()"> Очистити всі фільтри</button>
        </div>
        <div class="result-counter" id="resultCounter">
            Знайдено слів: <span id="resultCount">0</span>
        </div>
    </div>
    <div class="table-container">
        <table id="slangTable">
            <thead><tr><th>Англійський сленг</th><th>Український відповідник</th><th>Значення</th><th>Сфера</th><th>Емоційне забарвлення</th><th>Контекст (англ.)</th><th>Контекст (укр.)</th></tr></thead>
            <tbody id="tableBody"></tbody>
        </table>
    </div>
</div>

<div id="wordModal" class="modal">
    <div class="modal-content">
        <span class="close" onclick="closeModal()">&times;</span>
        <h3 id="modalTitle" style="color: #667eea;"></h3>
        <div id="modalContent"></div>
    </div>
</div>

<div id="infoModal" class="modal">
    <div class="modal-content">
        <span class="close" onclick="closeInfoModal()">&times;</span>
        <h2 style="color: #667eea; margin-bottom: 15px;"> Про словник</h2>
        <p style="margin-bottom: 15px; line-height: 1.5;">Цей словник містить молодіжний сленг з американських серіалів <strong>"Рівердейл"</strong> та <strong>"Я ніколи не..."</strong>. Тут можна знайти англійські сленгові вирази, їх українські відповідники, значення, сферу вживання, емоційне забарвлення та приклади з контекстом.</p>

        <h3 style="margin: 15px 0 10px;"> Як користуватися:</h3>
        <ul style="margin-left: 20px; line-height: 1.6;">
            <li><strong>Фільтри</strong> — обирайте сферу сленгу або емоційне забарвлення, щоб звузити пошук. Можна комбінувати фільтри для точнішого результату.</li>
            <li><strong>Пошук</strong> — введіть слово англійською або українською; автодоповнення підкаже варіанти</li>
            <li><strong>Альтернативні переклади</strong> — слова, виділені <span style="color:#667eea; text-decoration:underline;">підкресленим кольоровим текстом</span>, мають додаткові варіанти перекладу з прикладами. Натисніть на них, щоб розглянути слово детальніше</li>
            <li><strong>Контексти</strong> — кожне слово супроводжується прикладом з серіалу англійською та українською мовами для кращого розуміння де воно використовується</li>
        </ul>
        <button onclick="closeInfoModal()" style="margin-top: 20px; background: #667eea; color: white; padding: 8px 20px; border: none; border-radius: 8px; cursor: pointer;">Зрозуміло</button>
    </div>
</div>

<script>
    const allData = {json.dumps(data_list, ensure_ascii=False)};
    let currentData = [...allData];

    function escapeHtml(text) {{
        if (!text) return '';
        return text.replace(/[&<>]/g, function(m) {{
            return m === '&' ? '&amp;' : (m === '<' ? '&lt;' : '&gt;');
        }});
    }}

    function capitalizeFirst(text) {{
        if (!text) return '';
        return text.charAt(0).toUpperCase() + text.slice(1);
    }}

    function displayTable(data) {{
        const tbody = document.getElementById('tableBody');
        tbody.innerHTML = '';

        // Оновлюємо лічильник
        const countSpan = document.getElementById('resultCount');
        if (countSpan) {{
            countSpan.textContent = data.length;
        }}

        // Виводимо в консоль для інформації
        console.log('Знайдено слів: ' + data.length);

        if (data.length === 0) {{
            const row = tbody.insertRow();
            row.insertCell(0).colSpan = 7;
            row.insertCell(0).innerHTML = '<div style="text-align:center; padding:40px;"> Нічого не знайдено за вашим запитом</div>';
            return;
        }}

        data.forEach((item, index) => {{
            const row = tbody.insertRow();
            if (item.has_alternatives) {{
                row.insertCell(0).innerHTML = `<span class="clickable-word" onclick="showDetails(${{index}}, true)">${{escapeHtml(item.english)}}</span>`;
                row.insertCell(1).innerHTML = `<span class="clickable-word" onclick="showDetails(${{index}}, true)">${{escapeHtml(item.ukrainian)}}</span>`;
            }} else {{
                row.insertCell(0).innerHTML = escapeHtml(item.english) || '-';
                row.insertCell(1).innerHTML = escapeHtml(item.ukrainian) || '-';
            }}
            row.insertCell(2).innerHTML = escapeHtml(item.meaning) || '-';
            row.insertCell(3).innerHTML = escapeHtml(item.sphere) || '-';
            row.insertCell(4).innerHTML = escapeHtml(item.emotion) || '-';
            row.insertCell(5).innerHTML = item.context_en || '-';
            row.insertCell(6).innerHTML = item.context_ua || '-';
        }});
    }}

    function filterTable() {{
        const sphere = document.getElementById('sphereFilter').value;
        const emotion = document.getElementById('emotionFilter').value;
        const searchTerm = searchInput.value.toLowerCase().trim();

        let filtered = allData.filter(item => {{
            if (sphere && item.sphere !== sphere) return false;
            if (emotion && item.emotion !== emotion) return false;
            if (searchTerm && !item.english.toLowerCase().includes(searchTerm) && !item.ukrainian.toLowerCase().includes(searchTerm)) return false;
            return true;
        }});

        currentData = filtered;
        displayTable(currentData);
    }}

    const searchInput = document.getElementById('searchInput');
    const autocompleteList = document.getElementById('autocompleteList');

    searchInput.addEventListener('input', function() {{
        const value = this.value.toLowerCase().trim();

        if (!value) {{
            autocompleteList.style.display = 'none';
            autocompleteList.innerHTML = '';
            filterTable();
            return;
        }}

        const suggestions = new Set();
        allData.forEach(item => {{
            if (item.english.toLowerCase().startsWith(value)) {{
                suggestions.add(item.english);
            }}
            if (item.ukrainian.toLowerCase().startsWith(value)) {{
                suggestions.add(item.ukrainian);
            }}
        }});

        const suggestionsArray = Array.from(suggestions).slice(0, 10);

        if (suggestionsArray.length > 0) {{
            autocompleteList.innerHTML = suggestionsArray.map(word => 
                `<div class="autocomplete-item" onclick="selectSuggestion('${{word.replace(/'/g, "\\\\'")}}')">${{escapeHtml(word)}}</div>`
            ).join('');
            autocompleteList.style.display = 'block';
        }} else {{
            autocompleteList.innerHTML = `<div class="autocomplete-no-result"> Нічого не знайдено</div>`;
            autocompleteList.style.display = 'block';
        }}
    }});

    function selectSuggestion(word) {{
        searchInput.value = word;
        autocompleteList.style.display = 'none';
        autocompleteList.innerHTML = '';
        filterTable();
    }}

    document.addEventListener('click', function(e) {{
        if (!searchInput.contains(e.target) && !autocompleteList.contains(e.target)) {{
            autocompleteList.style.display = 'none';
            autocompleteList.innerHTML = '';
        }}
    }});

    function clearFilters() {{
        document.getElementById('sphereFilter').value = '';
        document.getElementById('emotionFilter').value = '';
        searchInput.value = '';
        autocompleteList.style.display = 'none';
        autocompleteList.innerHTML = '';
        filterTable();
    }}

    function showDetails(index, useCurrentData = true) {{
        const item = useCurrentData ? currentData[index] : allData[index];
        const modal = document.getElementById('wordModal');
        document.getElementById('modalTitle').innerHTML = `${{escapeHtml(item.english)}} / ${{escapeHtml(item.ukrainian)}}`;
        let content = `<p><strong> Значення:</strong> ${{escapeHtml(item.meaning) || 'Немає'}}</p><p><strong> Сфера:</strong> ${{escapeHtml(item.sphere) || 'Немає'}}</p><p><strong> Емоція:</strong> ${{escapeHtml(item.emotion) || 'Немає'}}</p>`;
        if (item.has_alternatives && item.alternatives_list.length) {{
            content += `<hr><h4> Альтернативні варіанти перекладу та вживання:</h4>`;
            item.alternatives_list.forEach((alt, i) => {{
                content += `<div class="alternative-item"><div class="alternative-word">Варіант ${{i+1}}: ${{escapeHtml(capitalizeFirst(alt.alternative))}}</div><div class="context-text"><div class="context-en">🇬🇧 ${{escapeHtml(alt.context_en) || 'Немає прикладу'}}</div><div class="context-ua">🇺🇦 ${{escapeHtml(alt.context_ua) || 'Немає прикладу'}}</div></div></div>`;
            }});
        }}
        document.getElementById('modalContent').innerHTML = content;
        modal.style.display = 'block';
    }}

    function closeModal() {{ 
        document.getElementById('wordModal').style.display = 'none'; 
    }}

    function openInfoModal() {{
        document.getElementById('infoModal').style.display = 'block';
    }}

    function closeInfoModal() {{
        document.getElementById('infoModal').style.display = 'none';
    }}

    window.onclick = function(e) {{ 
        if (e.target === document.getElementById('wordModal')) closeModal();
        if (e.target === document.getElementById('infoModal')) closeInfoModal();
    }}

    filterTable();
</script>
</body>
</html>'''

# Зберігаємо HTML файл
output_file = '/Users/macbook/Documents/диплом/Словник/index.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("\n Створено index.html")