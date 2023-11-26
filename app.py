from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configure the database URI using environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://user:password@postgres:5432/form-db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

class FormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    message = db.Column(db.Text)

# Flag to ensure table creation occurs only once
table_created = False

# Function to create tables before the first request
@app.before_request
def create_tables():
    global table_created
    if not table_created:
        with app.app_context():
            db.create_all()
        table_created = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            address = request.form['address']
            message = request.form['message']

            form_data = FormData(name=name, email=email, phone=phone, address=address, message=message)
            db.session.add(form_data)
            db.session.commit()

            return "Record added successfully"
        except Exception as e:
            db.session.rollback()  # Rollback the transaction in case of an exception
            return f"An error occurred: {str(e)}"

@app.route('/view')
def view():
    try:
        form_data_list = FormData.query.all()
        return render_template('view.html', form_data_list=form_data_list)
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    # Run the app in debug mode
    app.run(debug=True, host='0.0.0.0')
