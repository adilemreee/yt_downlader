from flask import Flask, request, render_template, send_file
import yt_dlp
import os

temp_folder = "downloads"
if not os.path.exists(temp_folder):
    os.makedirs(temp_folder)

cookie_file = "cookies.txt"  # YouTube çerezlerini buradan okuyacağız

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/download', methods=['POST'])
def download_video():
    url = request.form.get('url')
    if not url:
        return "Lütfen bir YouTube URL'si girin", 400

    try:
        file_path = os.path.join(temp_folder, "video.mp4")

        ydl_opts = {
            'outtmpl': file_path,
            'format': 'mp4',
            'cookiefile': cookie_file  # Çerezleri kullanarak giriş yap
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return send_file(file_path, as_attachment=True)

    except Exception as e:
        return f"Hata oluştu: {str(e)}", 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5300, debug=True)  # Dış dünyaya açık!
