from flask import Flask, session, redirect, render_template, request
from flask_mail import Mail, Message
from scripts.landing_page import landing_page
from scripts.contact_us import contact_us
from scripts.about_us import about_us
from scripts.help import help_page
from scripts.login import login_route  # Import the new login functio
from scripts.signup import signup, verify  # Import verify function
from scripts.dashboard import dashboard
from scripts.grader import grader
from scripts.profile import update_user_info  # Add this import
import os
import csv


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuration for Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'scrutatorapp@gmail.com'
app.config['MAIL_PASSWORD'] = 'cnpz uygl tejh ghcn'  # Your App Password
app.config['MAIL_DEFAULT_SENDER'] = 'scrutatorapp@gmail.com'

# Initialize Flask-Mail
mail = Mail(app)

UPLOAD_FOLDER = 'content/current'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

folder_path = "Accounts"
emails_file_path = os.path.join(folder_path, "mails", "emails.csv")

# Define function for signup route
def signup_route():
    return signup(folder_path, emails_file_path)  # Pass both paths

# Define function for grader route
def grader_route():
    return grader(app)


def get_user_data(username):
    try:
        with open(emails_file_path, mode='r', newline='') as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                if row['username'] == username:
                    return {
                        'username': row['username'],
                        'email': row['emailID'],  # Change this to match the CSV column name
                        'full_name': f"{row['first_name']} {row['last_name']}",
                        'password': row['password']  # Consider whether you need to expose this
                    }
    except FileNotFoundError:
        print("Email file not found!")
    return None  # Return None if no match is found


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    username = session.get('username')
    if username:
        if request.method == 'POST':
            # Handle the form submission
            full_name = request.form.get('full_name')
            specialization = request.form.get('specialization')
            gender = request.form.get('gender')
            school_name = request.form.get('school_name')
            dob = request.form.get('dob')
            city = request.form.get('city')

            # Call the update function in profile.py
            update_user_info(username, full_name, specialization, gender, school_name, dob, city)

            return redirect('/profile')  # Redirect back to the profile page after update

        # GET request: fetch user data to display on the profile page
        user_data = get_user_data(username)
        if user_data:
            return render_template('profile.html',
                                   username=user_data['username'],
                                   email=user_data['email'],
                                   full_name=user_data.get('full_name', ''),
                                   specialization=user_data.get('specialization', ''),
                                   gender=user_data.get('gender', ''),
                                   school_name=user_data.get('school_name', ''),
                                   dob=user_data.get('dob', ''),
                                   city=user_data.get('city', ''))

    return redirect('/login')  # Redirect to login if user is not logged in




# Routes
app.route('/')(landing_page)
app.route('/contact-us')(contact_us)
app.route('/about-us')(about_us)
app.route('/help')(help_page)
app.route('/login', methods=['GET', 'POST'])(login_route) # Use the named function
app.route('/register', methods=['GET', 'POST'])(signup_route)  # Use the named function
app.route('/dashboard')(dashboard)
app.route('/grader', methods=['GET', 'POST'])(grader_route)  # Use the named function
app.route('/verify', methods=['GET', 'POST'], endpoint='verify')(lambda: verify(emails_file_path))


if __name__ == '__main__':
    # Ensure the upload folder exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)