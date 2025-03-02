from flask import Flask, request, make_response, render_template_string, redirect, url_for
import base64
import json

app = Flask(__name__)

# Kullanıcı verileri ve gönderileri saklamak için sözlükler
users = {}
posts = {}

# Kullanıcıları Base64 ile şifreleme
def encode_cookie_data(data):
    json_data = json.dumps(data)
    encoded_data = base64.b64encode(json_data.encode()).decode()
    return encoded_data

def decode_cookie_data(encoded_data):
    try:
        json_data = base64.b64decode(encoded_data).decode()
        return json.loads(json_data)
    except:
        return None

# Basit kullanıcı bilgisi ve şifre saklama
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return "<h1>Bu kullanıcı adı zaten alınmış!</h1>"
        users[username] = password
        return "<h1>Kayıt başarılı! Lütfen giriş yapın.</h1><a href='/login'>Giriş Yap</a>"
    
    return '''
        <html>
            <head>
                <style>
                    body {
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background-color: #fafafa;
                        color: #333;
                        text-align: center;
                        padding: 20px;
                    }
                    h2 {
                        color: #4CAF50;
                    }
                    input[type="text"], input[type="password"] {
                        padding: 12px;
                        margin: 8px;
                        width: 280px;
                        border-radius: 4px;
                        border: 1px solid #ddd;
                    }
                    input[type="submit"] {
                        padding: 12px 25px;
                        background-color: #4CAF50;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        cursor: pointer;
                        transition: background-color 0.3s ease;
                    }
                    input[type="submit"]:hover {
                        background-color: #45a049;
                    }
                    .form-container {
                        max-width: 400px;
                        margin: 0 auto;
                        background-color: white;
                        padding: 20px;
                        border-radius: 10px;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    }
                </style>
            </head>
            <body>
                <h2>Kayıt Ol</h2>
                <div class="form-container">
                    <form method="post">
                        Kullanıcı adı: <input type="text" name="username" required><br>
                        Şifre: <input type="password" name="password" required><br>
                        <input type="submit" value="Kayıt Ol">
                    </form>
                </div>
            </body>
        </html>
    '''

# Giriş yapma ve cookie ile oturum açma
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username not in users or users[username] != password:
            return "<h1>Hatalı kullanıcı adı veya şifre!</h1>"
        
        # Cookie ile kullanıcıyı kaydet (Base64 ile şifrelenmiş)
        user_data = {'username': username}
        encoded_user_data = encode_cookie_data(user_data)
        
        resp = make_response(redirect(url_for('profile')))
        resp.set_cookie('user_data', encoded_user_data)
        return resp
    
    return '''
        <html>
            <head>
                <style>
                    body {
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background-color: #fafafa;
                        color: #333;
                        text-align: center;
                        padding: 20px;
                    }
                    h2 {
                        color: #4CAF50;
                    }
                    input[type="text"], input[type="password"] {
                        padding: 12px;
                        margin: 8px;
                        width: 280px;
                        border-radius: 4px;
                        border: 1px solid #ddd;
                    }
                    input[type="submit"] {
                        padding: 12px 25px;
                        background-color: #4CAF50;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        cursor: pointer;
                        transition: background-color 0.3s ease;
                    }
                    input[type="submit"]:hover {
                        background-color: #45a049;
                    }
                    .form-container {
                        max-width: 400px;
                        margin: 0 auto;
                        background-color: white;
                        padding: 20px;
                        border-radius: 10px;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    }
                </style>
            </head>
            <body>
                <h2>Giriş Yap</h2>
                <div class="form-container">
                    <form method="post">
                        Kullanıcı adı: <input type="text" name="username" required><br>
                        Şifre: <input type="password" name="password" required><br>
                        <input type="submit" value="Giriş Yap">
                    </form>
                </div>
            </body>
        </html>
    '''

# Profil sayfası (Kullanıcı giriş yaptıysa profil sayfasını göster)
@app.route('/profile')
def profile():
    user_data_cookie = request.cookies.get('user_data')
    if not user_data_cookie:
        return redirect(url_for('login'))
    
    # Cookie'den kullanıcı bilgisini çöz
    user_data = decode_cookie_data(user_data_cookie)
    if not user_data:
        return redirect(url_for('login'))
    
    username = user_data['username']
    
    # Kullanıcının paylaştığı gönderileri al
    user_posts = posts.get(username, [])
    
    return render_template_string("""
        <html>
            <head>
                <style>
                    body {
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background-color: #fafafa;
                        color: #333;
                        text-align: center;
                        padding: 20px;
                    }
                    h1 {
                        color: #4CAF50;
                    }
                    h2 {
                        font-size: 18px;
                        color: #333;
                    }
                    .post {
                        background-color: white;
                        margin: 10px 0;
                        padding: 10px;
                        border-radius: 8px;
                        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                        display: inline-block;
                        width: 70%;
                        text-align: left;
                    }
                    input[type="text"] {
                        padding: 12px;
                        margin: 8px;
                        width: 70%;
                        border-radius: 4px;
                        border: 1px solid #ddd;
                    }
                    input[type="submit"] {
                        padding: 12px 25px;
                        background-color: #4CAF50;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        cursor: pointer;
                        transition: background-color 0.3s ease;
                    }
                    input[type="submit"]:hover {
                        background-color: #45a049;
                    }
                    a {
                        text-decoration: none;
                        color: #4CAF50;
                        font-size: 16px;
                    }
                    a:hover {
                        color: #45a049;
                    }
                    .profile-container {
                        max-width: 800px;
                        margin: 0 auto;
                    }
                </style>
            </head>
            <body>
                <div class="profile-container">
                    <h1>{{ username }}'in Profil Sayfası</h1>
                    <h2>Gönderiler:</h2>
                    <div>
                        {% for post in user_posts %}
                            <div class="post">{{ post }}</div>
                        {% endfor %}
                    </div>
                    
                    <h3>Yeni Gönderi Paylaş:</h3>
                    <form method="post" action="/create_post">
                        İçerik: <input type="text" name="post_content" required><br>
                        <input type="submit" value="Paylaş">
                    </form>
                    
                    <a href="/logout">Çıkış Yap</a>
                </div>
            </body>
        </html>
    """, username=username, user_posts=user_posts)

# Gönderi oluşturma
@app.route('/create_post', methods=['POST'])
def create_post():
    user_data_cookie = request.cookies.get('user_data')
    if not user_data_cookie:
        return redirect(url_for('login'))
    
    user_data = decode_cookie_data(user_data_cookie)
    if not user_data:
        return redirect(url_for('login'))
    
    username = user_data['username']
    post_content = request.form['post_content']
    
    # Kullanıcıya ait gönderiyi ekle
    if username not in posts:
        posts[username] = []
    posts[username].append(post_content)
    
    return redirect(url_for('profile'))

# Çıkış yapma
@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('login')))
    resp.delete_cookie('user_data')
    return resp

# Ana sayfa (Giriş veya kayıt olma seçenekleri)
@app.route('/')
def home():
    user_data_cookie = request.cookies.get('user_data')
    if user_data_cookie:
        return redirect(url_for('profile'))
    
    return '''
        <html>
            <head>
                <style>
                    body {
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background-color: #fafafa;
                        color: #333;
                        text-align: center;
                        padding: 20px;
                    }
                    h2 {
                        color: #4CAF50;
                    }
                    a {
                        text-decoration: none;
                        color: #4CAF50;
                        font-size: 16px;
                    }
                    a:hover {
                        color: #45a049;
                    }
                </style>
            </head>
            <body>
                <h2>Hoş Geldiniz!</h2>
                <p><a href="/register">Kayıt Ol</a> | <a href="/login">Giriş Yap</a></p>
            </body>
        </html>
    '''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
