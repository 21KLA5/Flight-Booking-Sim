from flask import Flask, render_template, request, redirect, url_for
from pymongo.mongo_client import MongoClient

app = Flask(__name__)

#mock database
database = {}

#Setting up MongoDB
uri = "mongodb+srv://Group40-CH:3CdTLef740aHcdLK@group-40ch.icio9.mongodb.net/?retryWrites=true&w=majority&appName=Group-40CH"

# Create a new client and connect to the server
client = MongoClient(uri)

db = client["user_database"]  # Database name
users_collection = db["users"]  # Collection for storing users


@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        return render_template('index.html', user_input=user_input)
    return render_template('index.html', user_input=None)


# Profile Management route
@app.route('/profile/<email>', methods=['GET', 'POST'])
def profile(email):
    user = database.get(email)
    error_message = None

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'Save Changes':
            first_name = request.form['firstName']
            last_name = request.form['lastName']
            new_email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirmPass']

            # Validation: Ensure no field is blank and passwords match
            if not first_name or not last_name or not new_email or not password or not confirm_password:
                error_message = "All fields must be filled."
            elif password != confirm_password:
                error_message = "Passwords do not match."
            else:
                error_message = ""
                # Handle email change
                if new_email != email:
                    database[new_email] = database.pop(email)
                    database[new_email]['email'] = new_email  # Update the email field with new email
                    email = new_email

                # Update other user data 
                database[email]['firstName'] = first_name
                database[email]['lastName'] = last_name
                database[email]['password'] = password

                # Save successfull return to profile
                return redirect(url_for('profile', email=email))

        elif action == 'Discard Changes':
            # Discard changes and redirect to index
            return redirect(url_for('index'))

    return render_template('profile.html', user=database[email], email=email, error_message=error_message)

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        # Get form data
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        password = request.form['password']
        confirmPass = request.form['confirmPass']

        #Check if fields are empty 
        if not firstName or not lastName or not email or not password or not confirmPass:
            return render_template('register.html', errorMessage="Fill out all fields")

        #Check if passwords match
        if password != confirmPass:
            return render_template('register.html', errorMessage="Passwords do not match")

        # Check if the username already exists in the database
        elif email in database:
            return render_template('register.html', errorMessage="email already registered")

        else: 
            # Store user details in the mock database
            database[email] = {'firstName': firstName, 'lastName': lastName, 'password': password}
            # Redirect to login page
            return redirect(url_for('login'))

        
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user_email = request.form['email']
        user_password = request.form['password']

        if user_email not in database:
            
            return render_template('login.html', errorMessage="The provided email is not registered")
        else:
            if (database[user_email]['password'] == user_password):
                return redirect(url_for('profile', email=user_email))
            else:
                return render_template('login.html', errorMessage="Email and password does not match")

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)