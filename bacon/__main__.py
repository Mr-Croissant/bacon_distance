from pathlib import Path

import streamlit.web.cli

if __name__ == "__main__":
    filename = str(Path(__file__).parent / "app.py")
    streamlit.web.cli.main_run([filename])
