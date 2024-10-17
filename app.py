from flask import Flask, render_template, request

app = Flask(__name__)

#mock database
database = {'johndoe@gmail.com': {
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'johndoe@gmail.com',
        'password': 'password123'
    }}

@app.route('/', methods=['GET', 'POST'])
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
        if request.form.get('action') == 'Save Changes':
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
                # Update user data in the mock database
                user['firstName'] = first_name
                user['lastName'] = last_name
                user['email'] = new_email
                user['password'] = password

                # Save successful, redirect to index
                return redirect(url_for('index'))

        elif request.form.get('action') == 'Discard Changes':
            # Discard changes and redirect to index
            return redirect(url_for('index'))

    return render_template('profile.html', user=user, error_message=error_message)


if __name__ == '__main__':
    app.run(debug=True)