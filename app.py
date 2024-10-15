from flask import Flask, render_template, request, redirect, url_for

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

        #Check if passwords match
        if password != confirmPass:
            return "passwords do not match"

        # Check if the username already exists in the database
        if email in database:
            return "email already registered"
        
        if not firstName or not lastName or not email or not password or not confirmPass:
            return "missing required field"
        
        # Store user details in the mock database
        database[email] = {'firstName': firstName, 'lastName': lastName, 'password': password}
        
        # Redirect to login page (Terence put url here)
        return redirect(url_for(email=email))
    
    # For GET requests, display the registration form
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)