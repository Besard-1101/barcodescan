from flask import Flask, render_template, request, session
from flask_mail import Mail, Message
import os
import base64

app = Flask(__name__)
app.secret_key = 'geheim'

# Mail-Konfiguration aus Umgebungsvariablen
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

mail = Mail(app)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/confirm", methods=["POST"])
def confirm():
    code = request.form.get("code")
    session["code"] = code
    return render_template("confirm.html", code=code)

@app.route("/send", methods=["POST"])
def send():
    signature_data = request.form.get("signature")
    date = request.form.get("datecode", "Kein Code")

    msg = Message("Neuer Scan mit Unterschrift", recipients=[app.config['MAIL_USERNAME']])
    msg.body = f"Code: {code}\nDatum: {date}"

    if signature_data:
        header, encoded = signature_data.split(",", 1)
        image_data = base64.b64decode(encoded)
        msg.attach("unterschrift.png", "image/png", image_data)

    mail.send(msg)
    return "E-Mail erfolgreich gesendet!"

if __name__ == "__main__":
    app.run(debug=True)
