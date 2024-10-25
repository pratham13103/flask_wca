from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import quote_plus 

app = Flask(__name__)
app.secret_key = 'Pratham#123'  # Change this to a random secret key
username = quote_plus('Prathamesh13J')  
password = quote_plus('Jaiswalll@13') 
app.config['MONGO_URI'] = 'mongodb+srv://Prathamesh13J:Jaiswalll@13@cluster0.ststo.mongodb.net/chat_analyzer?retryWrites=true&w=majority&appName=Cluster0'
app.config["MONGO_CONNECT_TIMEOUT_MS"] = 5000  # 5 seconds
mongo = PyMongo(app)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password)

        # Check if the username already exists
        existing_user = mongo.db.users.find_one({'username': username})
        if existing_user:
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('home'))

        # Insert the new user into the database
        mongo.db.users.insert_one({'username': username, 'password': hashed_password})
        flash('Registration successful! Please log in.')
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = mongo.db.users.find_one({'username': username})  # Ensure it's 'users'

    if user and check_password_hash(user['password'], password):
        session['username'] = username
        return redirect("https://flaskwca-d7blman4xiq8zaxezcsifu.streamlit.app/")  # Redirect to Streamlit app
    else:
        flash('Invalid username or password.')
        return redirect(url_for('home'))


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=5001)  # Change to an available port


