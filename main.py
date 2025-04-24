import os
from docx import Document
from elevenlabs.client import ElevenLabs
from elevenlabs import save
import math

# Настройки
API_KEY = "sk_a35f2cb7ccc06ffaa5e3fb11daf3e5ed93ccfb51659ce549"
VOICE_ID = "21m00Tcm4TlvDq8ikWAM"

INPUT_FOLDER = "word_files"
OUTPUT_FOLDER = "audio_output"
CHUNK_SIZE = 4000  # ElevenLabs безопасно работи до ~5000 символа

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Извличане на текст
def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

# Разделяне на текста на части
def split_text(text, max_length):
    return [text[i:i + max_length] for i in range(0, len(text), max_length)]

# Обработка на един файл
def process_file(filepath, output_path):
    text = extract_text_from_docx(filepath)
    if not text.strip():
        print("⚠️ Файлът е празен.")
        return

    client = ElevenLabs(api_key=API_KEY)
    print(f"📤 Генериране на аудио части...")

    chunks = split_text(text, CHUNK_SIZE)
    audio_all = b""

    for i, chunk in enumerate(chunks, start=1):
        print(f"  ▶️ Част {i}/{len(chunks)}...")
        audio = client.text_to_speech.convert(
            text=chunk,
            voice_id=VOICE_ID,
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128"
        )
        audio_all += b"".join(audio)

    with open(output_path, "wb") as f:
        f.write(audio_all)

    print(f"[✅] Готово: {output_path}")

# Главна функция
def main():
    for filename in os.listdir(INPUT_FOLDER):
        if filename.endswith(".docx"):
            input_path = os.path.join(INPUT_FOLDER, filename)
            output_filename = os.path.splitext(filename)[0] + ".mp3"
            output_path = os.path.join(OUTPUT_FOLDER, output_filename)

            print(f"\n📄 Обработка на: {filename}")
            process_file(input_path, output_path)

if __name__ == "__main__":
    main()
