from flask import Flask, request, make_response, render_template_string, redirect, url_for
import sqlite3
import base64
import json

app = Flask(__name__)

# SQLite veritabanı bağlantısını aç
def get_db():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    return conn

# Kullanıcıyı veritabanına kaydet
def create_user(username, password):
    conn = get_db()
    conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()

# Kullanıcıyı veritabanında kontrol et
def check_user(username, password):
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
    conn.close()
    return user

# Kullanıcıları veritabanından al
def get_all_users():
    conn = get_db()
    users = conn.execute('SELECT username FROM users').fetchall()
    conn.close()
    return [user['username'] for user in users]

# Mesajları veritabanına kaydet
def create_message(from_user, to_user, message):
    conn = get_db()
    conn.execute('INSERT INTO messages (from_user, to_user, message) VALUES (?, ?, ?)', (from_user, to_user, message))
    conn.commit()
    conn.close()
def encode_cookie_data(data):
    """Veriyi Base64 ile şifreler."""
    json_data = json.dumps(data)
    encoded_data = base64.b64encode(json_data.encode('utf-8')).decode('utf-8')
    return encoded_data

# Kullanıcı mesajlarını veritabanından al
def get_messages(from_user, to_user):
    conn = get_db()
    messages = conn.execute('SELECT * FROM messages WHERE (from_user = ? AND to_user = ?) OR (from_user = ? AND to_user = ?)', 
                            (from_user, to_user, to_user, from_user)).fetchall()
    conn.close()
    return messages
def decode_cookie_data(data):
    """Base64 ile şifrelenmiş veriyi çözer."""
    try:
        decoded_data = base64.b64decode(data).decode('utf-8')
        return json.loads(decoded_data)
    except Exception as e:
        return None  # Hata durumunda None dönebilir

# Veritabanını ilk kez başlatma (eğer gerekli tablolarda yoksa)
def init_db():
    conn = get_db()
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, from_user TEXT, to_user TEXT, message TEXT)')
    conn.commit()
    conn.close()

init_db()  # Veritabanını başlat

@app.route('/')
def home():
    user_data_cookie = request.cookies.get('user_data')
    if not user_data_cookie:
        return redirect(url_for('login'))

    # Cookie'den kullanıcı bilgisini çöz
    user_data = decode_cookie_data(user_data_cookie)
    if not user_data:
        return redirect(url_for('login'))

    username = user_data['username']
    
    # Kayıtlı kullanıcıları veritabanından al
    users_list = get_all_users()
    
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
                    a {
                        text-decoration: none;
                        color: #4CAF50;
                        font-size: 16px;
                    }
                    a:hover {
                        color: #45a049;
                    }
                    .user-list {
                        margin-top: 20px;
                    }
                    .user {
                        padding: 10px;
                        background-color: #fff;
                        margin: 5px;
                        border-radius: 8px;
                        cursor: pointer;
                    }
                    .user:hover {
                        background-color: #4CAF50;
                        color: white;
                    }
                </style>
            </head>
            <body>
                <h1>Hoş Geldiniz, {{ username }}!</h1>
                <h2>Kayıtlı Kullanıcılar:</h2>
                <div class="user-list">
                    {% for user in users_list %}
                        <div class="user" onclick="window.location.href='/chat/{{ user }}'">{{ user }}</div>
                    {% endfor %}
                </div>
                <a href="/logout">Çıkış Yap</a>
            </body>
        </html>
    """, username=username, users_list=users_list)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = check_user(username, password)
        if not user:
            return "<h1>Hatalı kullanıcı adı veya şifre!</h1>"

        # Cookie ile kullanıcıyı kaydet (Base64 ile şifrelenmiş)
        user_data = {'username': username}
        encoded_user_data = encode_cookie_data(user_data)

        resp = make_response(redirect(url_for('home')))
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
                </style>
            </head>
            <body>
                <h2>Giriş Yap</h2>
                <form method="post">
                    Kullanıcı adı: <input type="text" name="username" required><br>
                    Şifre: <input type="password" name="password" required><br>
                    <input type="submit" value="Giriş Yap">
                </form>
                <br>
                <h3>Henüz kaydınız yok mu? <a href="/register">Kaydolun</a></h3>
            </body>
        </html>
    '''

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        create_user(username, password)
        return redirect(url_for('login'))

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
                </style>
            </head>
            <body>
                <h2>Kayıt Ol</h2>
                <form method="post">
                    Kullanıcı adı: <input type="text" name="username" required><br>
                    Şifre: <input type="password" name="password" required><br>
                    <input type="submit" value="Kayıt Ol">
                </form>
                <br>
                <a href="/login">Zaten hesabınız var mı? Giriş yapın</a>
            </body>
        </html>
    '''

@app.route('/chat/<username>', methods=['GET', 'POST'])
def chat(username):
    user_data_cookie = request.cookies.get('user_data')
    if not user_data_cookie:
        return redirect(url_for('login'))

    # Cookie'den kullanıcı bilgisini çöz
    user_data = decode_cookie_data(user_data_cookie)
    if not user_data:
        return redirect(url_for('login'))

    current_user = user_data['username']

    # Mesajlaşma
    if request.method == 'POST':
        message = request.form['message']
        create_message(current_user, username, message)

    chat_history = get_messages(current_user, username)

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
                    h2 {
                        color: #4CAF50;
                    }
                    .chat {
                        max-width: 600px;
                        margin: 0 auto;
                        background-color: white;
                        padding: 10px;
                        border-radius: 8px;
                    }
                    .message {
                        padding: 8px;
                        background-color: #f1f1f1;
                        border-radius: 5px;
                        margin: 5px 0;
                    }
                    input[type="text"] {
                        width: 80%;
                        padding: 8px;
                        margin: 10px 0;
                        border-radius: 4px;
                        border: 1px solid #ddd;
                    }
                    input[type="submit"] {
                        padding: 10px;
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
                    .notification {
                        background-color: #4CAF50;
                        color: white;
                        padding: 10px;
                        margin: 20px 0;
                        border-radius: 5px;
                        display: none;
                    }
                    a {
                        color: #4CAF50;
                    }
                </style>
                <script>
                    // Mesaj gönderildikten sonra bildirim göstermek için JavaScript
                    function showNotification(message) {
                        var notification = document.getElementById('notification');
                        notification.innerHTML = "Yeni mesaj: " + message;
                        notification.style.display = 'block';
                        setTimeout(function() {
                            notification.style.display = 'none';
                        }, 5000);
                    }

                    // AJAX ile mesaj gönderme
                    function sendMessage(event) {
                        event.preventDefault();
                        var message = document.getElementById("messageInput").value;
                        var xhr = new XMLHttpRequest();
                        xhr.open("POST", "", true);
                        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
                        xhr.onload = function() {
                            if (xhr.status === 200) {
                                showNotification(message);
                                document.getElementById("messageInput").value = ''; // Mesaj kutusunu temizle
                            }
                        };
                        xhr.send("message=" + encodeURIComponent(message));
                    }
                </script>
            </head>
            <body>
                <h2>{{ current_user }} ve {{ username }} arasındaki sohbet</h2>
                <div class="chat">
                    {% for message in chat_history %}
                        <div class="message"><strong>{{ message['from_user'] }}:</strong> {{ message['message'] }}</div>
                    {% endfor %}
                </div>
                <form onsubmit="sendMessage(event)">
                    <input id="messageInput" type="text" name="message" placeholder="Mesajınızı yazın" required><br>
                    <input type="submit" value="Gönder">
                </form>

                <!-- Bildirim Kutusu -->
                <div id="notification" class="notification"></div>
                
                <br>
                <a href="/">Ana sayfaya dön</a>
            </body>
        </html>
    """, username=username, current_user=current_user, chat_history=chat_history)


@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('login')))
    resp.delete_cookie('user_data')
    return resp

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
