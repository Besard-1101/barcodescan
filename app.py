
from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# Konfiguration für Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'deine@emailadresse.de'
app.config['MAIL_PASSWORD'] = 'dein_passwort'
app.config['MAIL_DEFAULT_SENDER'] = 'deine@emailadresse.de'

mail = Mail(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send_code", methods=["POST"])
def send_code():
    data = request.get_json()
    code = data.get("code", "")
    if code:
        try:
            msg = Message("Neuer Scan-Code", recipients=["deine@emailadresse.de"])
            msg.body = f"Gescannt: {code}"
            mail.send(msg)
            return jsonify({"status": "success"}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    return jsonify({"status": "error", "message": "Kein Code erhalten"}), 400

if __name__ == "__main__":
    app.run(debug=True)
