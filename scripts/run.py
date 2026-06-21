from pathlib import Path
import subprocess
import signal

from flask import Flask, send_from_directory
from flask_cors import CORS

from prepare_labeling_data import prepare_labeling_data

app = Flask(__name__)
CORS(app)

ROOT = Path(__file__).parent.parent


@app.route("/<path:filename>")
def serve_file(filename):
    return send_from_directory(ROOT, filename)


if __name__ == "__main__":
    prepare_labeling_data()

    # Label Studio起動
    ls_proc = subprocess.Popen(
        ["label-studio", "start"],
        preexec_fn=None,  # Linux/macOS
    )

    try:
        app.run(host="0.0.0.0", port=8000)
    finally:
        # Ctrl+C時にLabel Studioも終了
        ls_proc.send_signal(signal.SIGINT)
        try:
            ls_proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            ls_proc.kill()
