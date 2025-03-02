from flask import Flask, request, redirect
import os
import subprocess
import logging

app = Flask(__name__)

# Yüklenen dosyaların kaydedileceği klasör
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Kasıtlı zayıf kontrol:
# Dosya adında “.jpg” varsa kabul edilsin.
def allowed_file(filename):
    return '.jpg' in filename.lower()

@app.route('/')
def index():
    return '''
    <!doctype html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dosya Yükleme</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f7f6;
                color: #333;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                padding: 30px;
                width: 100%;
                max-width: 400px;
                text-align: center;
            }
            h1 {
                color: #4CAF50;
            }
            input[type="file"] {
                margin: 10px 0;
                padding: 10px;
                font-size: 16px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            input[type="submit"] {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
            }
            input[type="submit"]:hover {
                background-color: #45a049;
            }
            .message {
                margin-top: 20px;
                color: #333;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Dosya Yükle</h1>
            <form method="POST" enctype="multipart/form-data">
                <input type="file" name="file" />
                <input type="submit" value="Yükle" />
            </form>
        </div>
    </body>
    </html>
    '''

@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect('/')

    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        try:
            # Dosya kaydetme
            file.save(filepath)
            app.logger.info(f"Dosya '{filename}' başarıyla kaydedildi.")
        except Exception as e:
            app.logger.error(f"Dosya kaydedilirken hata oluştu: {e}")
            return "Dosya kaydedilirken bir hata oluştu.", 500
        
        # Eğer dosya adı .py ile bitiyorsa, çalıştırmaya çalışıyoruz.
        if filename.lower().endswith('.py'):
            try:
                # Windows ortamında çalıştırma (PowerShell kullanarak)
                subprocess.Popen(['powershell', filepath], shell=True)
                app.logger.info(f"Dosya '{filename}' çalıştırıldı.")
                return f"Dosya '{filename}' yüklendi ve çalıştırıldı!"
            except Exception as e:
                app.logger.error(f"Subprocess çalıştırılırken hata oluştu: {e}")
                return f"Dosya çalıştırılırken hata: {e}", 500
        
        return f"Dosya '{filename}' yüklendi!"
    
    else:
        return "Yalnızca .jpg içeren dosyalar kabul edilir."

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # Loglama ayarları
    app.logger.setLevel(logging.DEBUG)

    # LAN üzerinde herkese açık çalışacak şekilde başlatıyoruz
    app.run(host='0.0.0.0', port=6565)
