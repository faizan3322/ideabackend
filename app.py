from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)

# Enable CORS with explicit settings
CORS(app, resources={r"/submit-form": {"origins": "http://localhost:5173"}})

# Configure SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Database
db = SQLAlchemy(app)

# Define the Contact model
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

# Ensure tables are created at startup
with app.app_context():
    db.create_all()

# Route to handle form submission
@app.route('/submit-form', methods=['POST'])
def submit_form():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Invalid request"}), 400
        
        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        message = data.get("message", "").strip()

        # Validation checks
        if not name or not email or not message:
            return jsonify({"error": "All fields are required"}), 400

        # Save data to the database
        new_entry = Contact(name=name, email=email, message=message)
        db.session.add(new_entry)
        db.session.commit()

        return jsonify({"message": "Form submitted successfully!"}), 201
    
    except Exception as e:
        print(f"Error: {e}")  # Print error in Flask console
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(debug=True)
