from pathlib import Path
import streamlit.components.v1 as components

_COMPONENT = components.declare_component(
    "professional_voice_recorder",
    path=str(Path(__file__).parent / "frontend"),
)

def voice_recorder(key=None, **kwargs):
    return _COMPONENT(key=key, default=None, **kwargs)
