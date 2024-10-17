from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        return render_template('index.html', user_input=user_input)
    return render_template('index.html', user_input=None)

@app.route('/profile/<email>', methods=['GET', 'POST'])
def profile(email):
    user = database.get(email)
    if not user:
        return redirect(url_for('register'))

    if request.method == 'POST':
        # Get the updated form data
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        new_password = request.form['password']
        confirm_password = request.form['confirmPass']

        # If password fields are filled in, check if they match
        if new_password and new_password != confirm_password:
            return render_template('profile.html', user=user, errorMessage="Passwords do not match")

        # Update the user information
        user['firstName'] = firstName
        user['lastName'] = lastName
        if new_password:  # Only update password if the user entered a new one
            user['password'] = new_password

        database[email] = user
        return redirect(url_for('profile', email=email))

    return render_template('profile.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)