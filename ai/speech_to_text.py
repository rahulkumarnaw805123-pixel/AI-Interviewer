import sounddevice as sd
import soundfile as sf
import whisper
import tempfile

model = whisper.load_model("base")


def listen():
    try:
        samplerate = 16000
        duration = 10

        print("Listening...")

        audio = sd.rec(
            int(duration * samplerate),
            samplerate=samplerate,
            channels=1,
            dtype="float32"
        )

        sd.wait()

        temp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)

        sf.write(temp.name, audio, samplerate)

        result = model.transcribe(temp.name)

        return result["text"]

    except Exception as e:
        return f"Error: {e}"