import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, jsonify, send_from_directory
from dotenv import load_dotenv

try:
    from flask_cors import CORS
    _has_cors = True
except ImportError:
    _has_cors = False

try:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address
    _has_limiter = True
except ImportError:
    _has_limiter = False

load_dotenv()

app = Flask(__name__, template_folder="templates", static_folder="static")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if _has_cors:
    CORS(app)

if _has_limiter:
    limiter = Limiter(get_remote_address, app=app,
                      default_limits=["200 per day", "50 per hour"],
                      storage_uri="memory://")
    def rate_limit(rule):
        return limiter.limit(rule)
else:
    def rate_limit(rule):
        def decorator(f): return f
        return decorator


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/contact", methods=["POST"])
@rate_limit("5 per minute")
def contact():
    data = request.get_json()
    first_name = data.get("first_name", "").strip()
    last_name  = data.get("last_name", "").strip()
    email      = data.get("email", "").strip()
    subject    = data.get("subject", "").strip()
    message    = data.get("message", "").strip()

    if not all([first_name, last_name, email, message]):
        return jsonify({"success": False, "error": "All fields are required."}), 400
    if "@" not in email or "." not in email:
        return jsonify({"success": False, "error": "Invalid email address."}), 400
    if len(message) < 10:
        return jsonify({"success": False, "error": "Message too short."}), 400

    smtp_host = os.getenv("SMTP_HOST")
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    to_email  = os.getenv("TO_EMAIL", "varun.ch1405@gmail.com")

    if smtp_host and smtp_user and smtp_pass:
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"Portfolio Contact: {subject or 'New message'}"
            msg["From"]    = smtp_user
            msg["To"]      = to_email
            msg["Reply-To"] = email
            body = f"Name: {first_name} {last_name}\nEmail: {email}\nSubject: {subject}\n\nMessage:\n{message}"
            msg.attach(MIMEText(body, "plain"))
            with smtplib.SMTP_SSL(smtp_host, 465) as server:
                server.login(smtp_user, smtp_pass)
                server.sendmail(smtp_user, to_email, msg.as_string())
            logger.info(f"Contact email sent from {email}")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
    else:
        logger.info(f"Contact | From: {email} | Subject: {subject} | Msg: {message[:80]}...")

    return jsonify({"success": True, "message": "Message received! I'll get back to you soon."})


@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "service": "varun-portfolio"})


@app.route("/cv")
def download_cv():
    return send_from_directory("static", "varun_cv.pdf", as_attachment=True)


@app.errorhandler(404)
def not_found(e):
    return render_template("index.html"), 200

@app.errorhandler(429)
def rate_limit_exceeded(e):
    return jsonify({"success": False, "error": "Too many requests. Please wait."}), 429

@app.errorhandler(500)
def server_error(e):
    return jsonify({"success": False, "error": "Server error. Please try again."}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_ENV", "production") == "development"
    app.run(host="0.0.0.0", port=port, debug=debug)
