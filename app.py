from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
    return "🎯 YouTube Subtitle API is working! Use /subtitle?url=VIDEO_URL"

@app.route('/subtitle')
def subtitle():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "❌ Please provide a YouTube video URL using ?url="}), 400

    try:
        ydl_opts = {
            'skip_download': True,
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitlesformat': 'json',
            'quiet': True,
            'simulate': True,
            'forcejson': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            subtitles = info.get('subtitles') or info.get('automatic_captions')

            if not subtitles:
                return jsonify({"error": "⚠️ No subtitles found for this video."}), 404

            return jsonify({
                "title": info.get('title'),
                "video_id": info.get('id'),
                "subtitles": subtitles
            })

    except Exception as e:
        return jsonify({"error": f"🔥 Internal Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
