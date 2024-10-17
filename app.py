from flask import Flask, render_template, request, redirect, url_for
import unittest

app = Flask(__name__)

#mock database
database = {}


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
            return redirect(url_for('login', email=email))
        
    return render_template('register.html')

@app.route('/login')
def login():
    return "registration successfull"

if __name__ == '__main__':
    app.run(debug=True)