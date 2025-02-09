from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Email
from config import Config
import traceback

app = Flask(__name__)
app.config.from_object(Config)  # ✅ Load config

# ✅ Enhanced CORS Setup
CORS(
    app,
    resources={r"/*": {"origins": ["http://localhost:5173", "https://s3crets.com"]}},
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "OPTIONS", "DELETE", "PUT"],
)

# ✅ Initialize Database and Migrations
db.init_app(app)
migrate = Migrate(app, db)


# ✅ Default Route
@app.route("/", methods=["GET"])
def index():
    return jsonify({"success": True, "message": "Backend is running!"}), 200


# ✅ Handle Preflight (OPTIONS) Requests
@app.route("/submit-email", methods=["OPTIONS"])
@app.route("/get-emails", methods=["OPTIONS"])
def options_handler():
    return jsonify({"success": True}), 200


# ✅ Get All Emails
@app.route("/get-emails", methods=["GET"])
def get_emails():
    try:
        emails = Email.query.all()
        email_list = [{"id": e.id, "email": e.email} for e in emails]
        return jsonify({"success": True, "emails": email_list}), 200
    except Exception as e:
        print(f"❌ Error in /get-emails: {e}")
        return jsonify({"success": False, "message": "Internal Server Error"}), 500


# ✅ Submit Email
@app.route("/submit-email", methods=["POST"])
def submit_email():
    email = request.json.get("email")

    if not email:
        return jsonify({"success": False, "message": "No email provided"}), 400

    try:
        new_email = Email(email=email)
        db.session.add(new_email)
        db.session.commit()
        return jsonify({"success": True, "message": "Email saved successfully."}), 201
    except Exception as e:
        print(f"❌ Error in /submit-email: {e}")
        print(traceback.format_exc())  # ✅ Logs full error traceback
        db.session.rollback()
        return jsonify({"success": False, "message": "Internal Server Error"}), 500


# ✅ Run Server
if __name__ == "__main__":
    app.run(debug=True)
