import asyncio
import base64
import os
import tempfile
import streamlit.components.v1 as components

# Microsoft neural male voice
VOICE = "en-US-GuyNeural"


def speak_clear(text: str):
    """Generate a clear, deep, professional male neural voice."""

    try:
        import edge_tts
    except ImportError as e:
        raise RuntimeError(
            "edge-tts is not installed. Run: pip install edge-tts"
        ) from e

    text = str(text).strip()

    if not text:
        return

    fd, path = tempfile.mkstemp(suffix=".mp3")
    os.close(fd)

    try:

        async def make_audio():
            tts = edge_tts.Communicate(
                text=text,
                voice=VOICE,
                rate="-8%",
                volume="+0%",
                pitch="-10Hz",
            )
            await tts.save(path)

        asyncio.run(make_audio())

        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode("ascii")

        # Hidden audio element: no audio player / progress bar is shown.
        html = f"""
        <html>
        <body style="
            margin:0;
            padding:0;
            background:transparent;
            overflow:hidden;
        ">
            <audio autoplay playsinline
                style="
                    display:none !important;
                    width:0;
                    height:0;
                ">
                <source
                    src="data:audio/mpeg;base64,{data}"
                    type="audio/mpeg"
                >
            </audio>
        </body>
        </html>
        """

        components.html(
            html,
            height=1,
            scrolling=False,
        )

    finally:
        try:
            os.remove(path)
        except OSError:
            pass
