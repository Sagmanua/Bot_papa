import json
from docx import Document

def parse_docx_with_colors(file_path):
    doc = Document(file_path)
    data = []
    current_item = None

    # Стандартні кольори RGB для Word
    GREEN_RGB = "00B050" 

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        # Визначаємо початок питання (наприклад, 1.1, 1.2)
        if any(char.isdigit() for char in text[:3]):
            if current_item:
                data.append(current_item)
            current_item = {"question": text, "options": []}
        
        # Визначаємо варіанти відповідей
        elif current_item is not None:
            is_correct = False
            for run in para.runs:
                if run.font.color and run.font.color.rgb:
                    if str(run.font.color.rgb) == GREEN_RGB:
                        is_correct = True
            
            current_item["options"].append({
                "text": text.lstrip('- '),
                "is_correct": is_correct
            })

    if current_item:
        data.append(current_item)
    return data

# Запуск
parsed_data = parse_docx_with_colors('107.docx')

# Збереження даних у файл JSON
output_filename = 'data.json'
with open(output_filename, 'w', encoding='utf-8') as f:
    json.dump(parsed_data, f, indent=4, ensure_ascii=False)

print(f"Дані успішно збережено у файл {output_filename}")