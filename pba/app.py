# Import what we need from flask
from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime
import json
from werkzeug.security import generate_password_hash, check_password_hash

# Create the Flask app
app = Flask(__name__)
# We need this for login to work
app.secret_key = 'your_secret_key'

# Store user data (like a simple database)
users = {}
events = []
band_requests = []

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    # If user submits the form
    if request.method == 'POST':
        # Get username and password from form
        username = request.form['username']
        password = request.form['password']
        
        # Check if user exists and password is correct
        if username in users and check_password_hash(users[username]['password'], password):
            # Save username in session (remember who is logged in)
            session['username'] = username
            # Show success message
            flash('Login successful!')
            # Go to profile page
            return redirect(url_for('profile', username=username))
        # If login fails, show error
        flash('Invalid username or password!')
    # Show login page
    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    # Remove username from session (forget who was logged in)
    session.pop('username', None)
    # Show logout message
    flash('You have been logged out.')
    # Go back to home page
    return redirect(url_for('home'))

# Profile page
@app.route('/profile/<username>')
def profile(username):
    # Check if user exists
    if username not in users:
        flash('User not found!')
        return redirect(url_for('home'))
    # Show profile page
    return render_template('profile.html', user=users[username])

# Register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    # If user submits the form
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']
        
        # Check if username already exists
        if username in users:
            flash('Username already exists!')
            return render_template('register.html')
        
        # Save new user data
        hashed_password = generate_password_hash(password)
        users[username] = {
            'username': username,
            'password': hashed_password,
            'instruments': request.form.get('instruments', ''),
            'experience': request.form.get('experience', ''),
            'genre': request.form.get('genre', ''),
            'bio': request.form.get('bio', '')
        }
        
        # Show success message
        flash('Registration successful! Please login.')
        # Go to login page
        return redirect(url_for('login'))
    
    # Show register page
    return render_template('register.html')

# Events page
@app.route('/events', methods=['GET', 'POST'])
def events_page():
    # If user submits new event
    if request.method == 'POST':
        # Get event details
        event = {
            'title': request.form['title'],
            'date': request.form['date'],
            'location': request.form['location'],
            'description': request.form['description']
        }
        # Add event to list
        events.append(event)
        flash('Event added successfully!')
    
    # Show events page with list of events
    return render_template('events.html', events=events)

# Band requests page
@app.route('/band-requests', methods=['GET', 'POST'])
def band_requests_page():
    # If user submits new request
    if request.method == 'POST':
        # Get request details
        request_data = {
            'band_name': request.form['band_name'],
            'instrument_needed': request.form['instrument_needed'],
            'genre': request.form['genre'],
            'description': request.form['description'],
            'contact': request.form['contact']
        }
        # Add request to list
        band_requests.append(request_data)
        flash('Band request added successfully!')
    
    # Show band requests page with list of requests
    return render_template('band_requests.html', requests=band_requests)

# Start the website
if __name__ == '__main__':
    app.run(debug=True)
