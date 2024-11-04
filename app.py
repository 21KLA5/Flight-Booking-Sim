from flask import Flask, render_template, request, redirect, url_for
from pymongo.mongo_client import MongoClient
import certifi


app = Flask(__name__)

#mock database
database = {}

#Setting up MongoDB
uri = "mongodb+srv://Group40-CH:3CdTLef740aHcdLK@group-40ch.icio9.mongodb.net/?retryWrites=true&w=majority&appName=Group-40CH"

# Create a new client and connect to the server
client = MongoClient(uri, tlsCAFile=certifi.where())

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
    user = users_collection.find_one({"email" : email})
    error_message = None
    db_user = users_collection.find_one({"email": user})

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
                # Update the user's information
                update_fields = {
                    "firstName": first_name,
                    "lastName": last_name,
                    "email": new_email,
                    "password": password
                }
                users_collection.update_one({"email": email}, {"$set": update_fields})

                # Redirect back to the profile page with the updated email
                return redirect(url_for('profile', email=new_email))

        elif action == 'Discard Changes':
            # Discard changes and redirect to index
            return redirect(url_for('index'))

    return render_template('profile.html', user=db_user, email=email, error_message=error_message)


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
        existing_user = users_collection.find_one({"email": email})
        if existing_user:
            return render_template('register.html', errorMessage="email already registered")

        
        # Store user details in the mock database
        users_collection.insert_one({
            "firstName": firstName,
            "lastName": lastName,
            "email": email,
            "password": password
        })
        # Redirect to login page
        return redirect(url_for('login'))

        
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user_email = request.form['email']
        user_password = request.form['password']

        db_user = users_collection.find_one({"email": user_email})

        # Checks if the entered email is registered with a user in the database 
        if db_user is None:
             return render_template('login.html', errorMessage="The provided email is not registered")
        # Checks if the password in database matches the password entered
        else:
            if db_user['password'] == user_password:
                return redirect(url_for('profile', email=user_email))
            else:
                return render_template('login.html', errorMessage="Email and password does not match")

    return render_template('login.html')
        

if __name__ == '__main__':
    app.run(debug=True)