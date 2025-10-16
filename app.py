from flask import Flask, render_template, request, session
from flask_mail import Mail, Message
import os
import base64

app = Flask(__name__)
app.secret_key = 'geheim'  # Für Sessions

# Mail-Konfiguration (kann auch aus .env geladen werden)
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.example.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'dein@email.de')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'deinpasswort')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'dein@email.de')

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
    date = request.form.get("datecode", "Kein Datum")
    code = session.get("code", "Kein Code")

    msg = Message("Neuer Scan mit Unterschrift", recipients=[app.config['MAIL_USERNAME']])
    msg.body = f"Code: {code}\nDatum: {date}"

    if signature_data:
        try:
            header, encoded = signature_data.split(",", 1)
            image_data = base64.b64decode(encoded)
            msg.attach("unterschrift.png", "image/png", image_data)
        except Exception as e:
            return f"Fehler beim Verarbeiten der Unterschrift: {str(e)}"

    try:
        mail.send(msg)
        return "E-Mail erfolgreich gesendet!"
    except Exception as e:
        return f"Fehler beim Senden der E-Mail: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
``
