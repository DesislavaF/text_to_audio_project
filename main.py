import os
import requests
from docx import Document

# Твоят ElevenLabs API ключ
API_KEY = 'YOUR_API_KEY'
VOICE_ID = 'Milena'

# Папка с Word файлове
INPUT_FOLDER = 'word_files'
OUTPUT_FOLDER = 'audio_output'

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return '\n'.join([para.text for para in doc.paragraphs])

def text_to_speech(text, output_path):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.56,
            "similarity_boost": 0.70,
            "style": 0.30,
            "use_speaker_boost": True
        },
        "output_format": "mp3_44100_128",
        "voice_speed": 1.13,
        "volume": "0dB"
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(response.content)
        print(f"Аудио запазено: {output_path}")
    else:
        print(f"Грешка при обработка: {response.status_code} - {response.text}")

def main():
    for filename in os.listdir(INPUT_FOLDER):
        if filename.endswith('.docx'):
            file_path = os.path.join(INPUT_FOLDER, filename)
            print(f"Обработка на файл: {filename}")
            text = extract_text_from_docx(file_path)
            output_file = os.path.join(OUTPUT_FOLDER, f"{os.path.splitext(filename)[0]}.mp3")
            text_to_speech(text, output_file)

if __name__ == '__main__':
    main()
