from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["POST"])
def get_subtitles():
    try:
        data = request.get_json()
        video_url = data.get("url")
        
        if not video_url:
            return jsonify({"error": "❌ URL missing!"}), 400

        ydl_opts = {
            'skip_download': True,
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': ['en'],
            'quiet': True,
            'forcejson': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            subtitles = info.get("automatic_captions", {}).get("en") or info.get("subtitles", {}).get("en")

            if not subtitles:
                return jsonify({"error": "⚠️ Subtitle not found!"}), 404

            return jsonify({
                "title": info.get("title"),
                "channel": info.get("uploader"),
                "subtitles_url": subtitles[0].get("url")
            })

    except Exception as e:
        return jsonify({"error": f"❌ Error: {str(e)}"}), 500

@app.route("/", methods=["GET"])
def home():
    return "✅ YT Subtitle API is running!"

if __name__ == "__main__":
    app.run()
