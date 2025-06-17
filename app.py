cat > app.py << 'EOF'
from flask import Flask, request, jsonify
from yt_dlp import YoutubeDL
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "🎉 API is live and working!"

@app.route('/subtitle', methods=['GET'])
def get_subtitle():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "URL parameter is missing"}), 400

    try:
        ydl_opts = {
            'skip_download': True,
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': ['en'],
            'subtitlesformat': 'srt',
            'outtmpl': '%(title)s.%(ext)s'
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            ydl.download([video_url])

        subtitle_file = None
        for ext in ['en.srt', 'en.vtt']:
            possible_file = f"{info['title']}.{ext}"
            if os.path.exists(possible_file):
                subtitle_file = possible_file
                break

        if subtitle_file:
            with open(subtitle_file, 'r', encoding='utf-8') as f:
                content = f.read()
            os.remove(subtitle_file)
            return jsonify({"subtitles": content})
        else:
            return jsonify({"error": "Subtitle not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
EOF
