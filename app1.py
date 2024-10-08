from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'Pratham#123'  # Change this to a random secret key
app.config['MONGO_URI'] = 'mongodb://localhost:27017/chat_analyzer'  # Update with your MongoDB URI
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
        mongo.db.USERS.insert_one({'username': username, 'password': hashed_password})
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
    user = mongo.db.USERS.find_one({'username': username})

    if user and check_password_hash(user['password'], password):
        session['username'] = username
        return redirect("http://localhost:8501")  # Change this to your Streamlit app's URL
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
    app.run(debug=True)
