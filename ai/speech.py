import asyncio
import edge_tts
import tempfile
import os
from pygame import mixer


def speak(text):

    async def _speak():

        communicate = edge_tts.Communicate(
            text,
            voice="en-US-JennyNeural"
        )

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as file:
            filename = file.name

        await communicate.save(filename)

        mixer.init()
        mixer.music.load(filename)
        mixer.music.play()

        while mixer.music.get_busy():
            await asyncio.sleep(0.1)

        mixer.music.stop()
        mixer.quit()

        os.remove(filename)

    asyncio.run(_speak())