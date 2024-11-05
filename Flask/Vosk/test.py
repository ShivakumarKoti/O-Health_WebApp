import os
import sys
import queue
import threading
import json

from vosk import Model, KaldiRecognizer
import pyaudio

# Optional: For English translation
from googletrans import Translator

def main():
    # Path to the Vosk Hindi model
    model_path = "vosk-model-small-hi-0.22"

    if not os.path.exists(model_path):
        print(f"Please download the Hindi model from https://alphacephei.com/vosk/models and unpack it as '{model_path}' in the current folder.")
        sys.exit(1)

    # Initialize the model
    model = Model(model_path)

    # Initialize recognizer with sample rate
    sample_rate = 16000  # Vosk model's expected sample rate
    recognizer = KaldiRecognizer(model, sample_rate)

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open microphone stream
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=8000)
    stream.start_stream()

    print("Speak into the microphone...")

    # Initialize translation
    translator = Translator()

    try:
        while True:
            data = stream.read(4000, exception_on_overflow=False)
            if len(data) == 0:
                break

            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                result_dict = json.loads(result)
                text_hindi = result_dict.get("text", "")
                if text_hindi:
                    print(f"Hindi: {text_hindi}")

                    # Optional: Translate to English
                    translation = translator.translate(text_hindi, src='hi', dest='en')
                    print(f"English: {translation.text}")
            else:
                # Partial result can be used if needed
                partial_result = recognizer.PartialResult()
                # Uncomment below to see partial results
                # print(partial_result)
                pass

    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    main()
