from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lottery.db'  # SQLite database
db = SQLAlchemy(app)

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    allocated_numbers = db.Column(db.String(255), nullable=False)

# Track the last allocated number
last_allocated_number = 0

@app.route('/')
def index():
    with app.app_context():  # Create an application context
        participants = Participant.query.all()
    return render_template('index.html', participants=participants, deleted=request.args.get('deleted'))

@app.route('/enter_lottery', methods=['GET', 'POST'])
def enter_lottery():
    global last_allocated_number  # Use the global last_allocated_number

    if request.method == 'POST':
        name = request.form['name']
        num_tickets = int(request.form['num_tickets'])

        # Calculate the allocated numbers for the current participant
        allocated_numbers = list(range(last_allocated_number + 1, last_allocated_number + 1 + num_tickets))

        # Update the last allocated number for the next participant
        last_allocated_number += num_tickets

        # Convert allocated_numbers to a string with comma separation
        allocated_numbers_str = ', '.join(map(str, allocated_numbers))

        with app.app_context():  # Create an application context
            participant = Participant(name=name, allocated_numbers=allocated_numbers_str)
            db.session.add(participant)
            db.session.commit()

        return redirect(url_for('index'))

    return render_template('enter_lottery.html')

if __name__ == '__main__':
    with app.app_context():  # Create an application context
        db.create_all()
    app.run(debug=True)
