from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Transaction
from sms_parser import parse_sms
from ai_engine import simple_insights
import os

app = Flask(__name__)
CORS(app)

# Database path setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return jsonify({"status": "Blitz AI backend running"})

@app.route("/parse-sms", methods=["POST"])
def parse_sms_api():
    payload = request.json
    sms = payload.get("sms", "")
    result = parse_sms(sms)
    return jsonify(result)

@app.route("/add", methods=["POST"])
def add_transaction():
    data = request.json

    txn = Transaction(
        amount=data.get("amount"),
        category=data.get("category", "others"),
        message=data.get("message", ""),
        date=data.get("date", "")
    )

    db.session.add(txn)
    db.session.commit()

    return jsonify({"status": "success", "id": txn.id})

@app.route("/transactions", methods=["GET"])
def get_transactions():
    txns = Transaction.query.all()
    return jsonify([t.to_dict() for t in txns])

@app.route("/insights", methods=["GET"])
def insights():
    txns = Transaction.query.all()
    data = [t.to_dict() for t in txns]
    return jsonify(simple_insights(data))

if __name__ == "__main__":
    app.run(debug=True, port=5000)

