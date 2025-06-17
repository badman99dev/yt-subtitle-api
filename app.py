from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return "✅ YT Subtitle API is working."

@app.route("/api", methods=["POST"])
def get_subtitles():
    try:
        data = request.get_json()
        url = data.get("url")

        if not url:
            return jsonify({"error": "❌ URL is required"}), 400

        # yt-dlp options
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "writesubtitles": True,
            "writeautomaticsub": True,
            "subtitlesformat": "json",
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        return jsonify({
            "title": info.get("title"),
            "channel": info.get("channel"),
            "subtitles": info.get("subtitles", {})
        })

    except Exception as e:
        return jsonify({"error": f"😵 Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
