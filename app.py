from flask import Flask, request
import subprocess
import os

app = Flask(__name__)

@app.route('/subs')
def get_subtitles():
    video_url = request.args.get('url')
    if not video_url:
        return "❌ Please provide a YouTube URL using ?url=...", 400

    # पुराने सबटाइटल्स हटाओ
    for f in os.listdir():
        if f.endswith(".vtt") or f.endswith(".srt"):
            os.remove(f)

    try:
        # yt-dlp से subtitle निकालो
        subprocess.run([
            'yt-dlp',
            '--write-auto-sub',
            '--skip-download',
            '--sub-lang', 'en',
            '--convert-subs', 'srt',
            video_url
        ], check=True)

        # सर्च करके subtitle दिखाओ
        for f in os.listdir():
            if f.endswith('.srt'):
                with open(f, 'r', encoding='utf-8') as subfile:
                    return f"✅ Subtitles from: {f}\n\n" + subfile.read()

        return "⚠️ No subtitles found.", 404

    except Exception as e:
        return f"❌ Error: {str(e)}", 500

app.run(host='0.0.0.0', port=3000)
