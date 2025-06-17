from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os
import uuid

app = Flask(__name__)
CORS(app)  # Allow requests from frontend JS

@app.route('/')
def index():
    return 'YouTube Subtitle API is Live!'

@app.route('/get_subtitle', methods=['POST'])
def get_subtitle():
    try:
        data = request.get_json()
        video_url = data.get('url')

        if not video_url:
            return jsonify({"error": "No URL provided"}), 400

        # Temporary file path for subtitles
        subtitle_filename = f"{uuid.uuid4()}.en.vtt"

        ydl_opts = {
            'writesubtitles': True,
            'subtitleslangs': ['en'],
            'skip_download': True,
            'outtmpl': subtitle_filename,
            'quiet': True,
            'forcejson': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)

        # Subtitle text
        if 'requested_subtitles' in info and 'en' in info['requested_subtitles']:
            if os.path.exists(subtitle_filename):
                with open(subtitle_filename, 'r', encoding='utf-8') as f:
                    subtitle_text = f.read()
                os.remove(subtitle_filename)
            else:
                subtitle_text = "Subtitle file not found."
        else:
            subtitle_text = "No English subtitles available."

        return jsonify({
            "title": info.get("title"),
            "channel": info.get("channel"),
            "thumbnail": info.get("thumbnail"),
            "subtitles": subtitle_text
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)
