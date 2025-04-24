import os
from dotenv import load_dotenv
from docx import Document
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

# === Настройки ===
load_dotenv()
API_KEY = os.getenv("ELEVENLABS_API_KEY") or "sk_a35f2cb7ccc06ffaa5e3fb11daf3e5ed93ccfb51659ce549"
VOICE_ID = "21m00Tcm4TlvDq8ikWAM"

INPUT_FOLDER = "word_files"
OUTPUT_FOLDER = "audio_output"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# === Четене на текст от .docx файл ===
def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

# === Конвертиране на текст в реч и запис ===
def text_to_speech_file(text: str, output_path: str):
    client = ElevenLabs(api_key=API_KEY)

    response = client.text_to_speech.convert(
        voice_id=VOICE_ID,
        output_format="mp3_44100_128",
        text=text,
        model_id="eleven_turbo_v2_5",
        voice_settings=VoiceSettings(
            stability=0.3,
            similarity_boost=0.8,
            style=0.3,
            use_speaker_boost=True,
            speed=1.0,
        ),
    )

    with open(output_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    print(f"[✅] Готово: {output_path}")

# === Главна функция ===
def main():
    for filename in os.listdir(INPUT_FOLDER):
        if filename.endswith(".docx"):
            input_path = os.path.join(INPUT_FOLDER, filename)
            output_filename = os.path.splitext(filename)[0] + ".mp3"
            output_path = os.path.join(OUTPUT_FOLDER, output_filename)

            print(f"\n📄 Обработка на: {filename}")
            text = extract_text_from_docx(input_path)

            if not text.strip():
                print("⚠️ Празен файл. Пропуснат.")
                continue

            text_to_speech_file(text, output_path)

if __name__ == "__main__":
    main()
