from flask import Flask, request, render_template, send_from_directory, redirect, url_for
import os
import subprocess
from werkzeug.utils import secure_filename

app = Flask(__name__)
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), "downloads")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        url = request.form.get("url")
        if url:
            try:
                subprocess.run([
                    "yt-dlp",
                    "-o", f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s",
                    url
                ], check=True)
                message = "✅ Download completed successfully!"
            except Exception as e:
                message = f"❌ Download failed: {str(e)}"
    return render_template("index.html", message=message)

@app.route("/downloads")
def downloads():
    files = os.listdir(DOWNLOAD_FOLDER)
    return render_template("downloads.html", files=files)

@app.route("/downloads/<filename>")
def serve_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, secure_filename(filename), as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080,debug=True)
