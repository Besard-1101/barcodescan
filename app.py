from flask import Flask, request, send_from_directory
import base64
import smtplib
from email.message import EmailMessage
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    address = data['address']
    date = data['date']
    signature_data = data['signature'].split(',')[1]
    signature_bytes = base64.b64decode(signature_data)

    filename = f"signature_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    with open(filename, 'wb') as f:
        f.write(signature_bytes)

    msg = EmailMessage()
    msg['Subject'] = '📦 Neue Lieferbestätigung'
    msg['From'] = os.getenv('EMAIL_USER')  # sichere Nutzung
    msg['To'] = 'besard.qazimi@siegwerk.com'
    msg.set_content(f"Lieferadresse: {address}\nDatum: {date}")

    with open(filename, 'rb') as f:
        msg.add_attachment(f.read(), maintype='image', subtype='png', filename=filename)

    try:
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.office365.com')
        smtp_port = int(os.getenv('SMTP_PORT', 587))
        email_user = os.getenv('EMAIL_USER')
        email_pass = os.getenv('EMAIL_PASS')

        with smtplib.SMTP(smtp_server, smtp_port) as smtp:
            smtp.starttls()
            smtp.login(email_user, email_pass)
            smtp.send_message(msg)

        os.remove(filename)
        return '✅ E-Mail erfolgreich gesendet!'
    except Exception as e:
        return f'❌ Fehler beim Senden der E-Mail: {e}'

if __name__ == '__main__':
    app.run(debug=True)
