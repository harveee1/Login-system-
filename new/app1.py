from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy, session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///response.sql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Model
class Response(db.Model):
    __tablename__ = 'response'  # Specify the table name

    id = db.Column(db.Integer, primary_key=True)
    emailId = db.Column(db.String(100), nullable=False)
    phoneNumber = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"Response(emailId='{self.emailId}', phoneNumber='{self.phoneNumber}', password='{self.password}', gender='{self.gender}')"

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/responses', methods=['POST'])
def read_form():
    data = request.form

    # Create a new Response instance
    response = Response(
        emailId=data['userEmail'],
        phoneNumber=data['userContact'],
        password=data['userPassword'],
        gender='Male' if 'genderMale' in data else 'Female'
    )

    # Add the response to the database
    db.session.add(response)
    db.session.commit()

    # Redirect to view-responses route
    return redirect(url_for('view_responses'))

@app.route('/view-responses', methods=['GET'])
def view_responses():
    # Retrieve all responses from the database
    responses = Response.query.all()

    # Display all stored responses
    return render_template('responses.html', responses=responses)

if __name__ == '__main__':
    app.debug = True
    app.run()
