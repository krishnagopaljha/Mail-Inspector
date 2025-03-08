import os
import email
import configparser
from flask import Flask, request, render_template, redirect, url_for, session
from email.header import decode_header
from werkzeug.utils import secure_filename
from groq import Groq

# Load API key from config.ini
config = configparser.ConfigParser()
config.read("config.ini")
GROQ_API_KEY = config.get("groq", "api_key", fallback=None)

if not GROQ_API_KEY:
    raise ValueError("Missing Groq API key in config.ini")

# Initialize Groq API client
client = Groq(api_key=GROQ_API_KEY)

# Flask App Initialization
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Used for session management
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def analyze_with_groq(subject, body):
    """Analyzes email using Groq AI."""
    prompt = f"""
    Conduct a phishing risk analysis on the following email and provide:
    - A phishing risk score (0-10), where 0 is safe and 10 is highly suspicious.
    - A brief, third-person explanation (max 10 words) highlighting the most relevant phishing indicator(s).
    - A detailed 3-4 line explanation explaining why the email was rated that way.
    
    Email:
    ---
    Subject: {subject}

    Body: {body}
    ---
    
    Response must follow this exact format:
    Score: X/10
    Overview: [Brief third-person summary, max 10 words]
    Explanation: [3-4 line detailed analysis]
    """
    
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile"
        )
        
        output = response.choices[0].message.content.strip()
        score, overview, explanation = 0, "No overview provided.", "No detailed explanation provided."
        
        try:
            score_line = next(line for line in output.split("\n") if "Score:" in line)
            score = int(score_line.split(":")[1].strip().split("/")[0])
            
            overview_line = next(line for line in output.split("\n") if "Overview:" in line)
            overview = overview_line.split(":")[1].strip()
            
            explanation_line = next(line for line in output.split("\n") if "Explanation:" in line)
            explanation = explanation_line.split(":", 1)[1].strip()
        except Exception:
            explanation = "AI response format error."
        
        return overview, explanation, score
    except Exception as e:
        return "AI Analysis Error", f"Error: {str(e)}", 0

def extract_email_content(email_path):
    """Extracts subject & body from an .eml file."""
    try:
        with open(email_path, 'r', encoding='utf-8') as f:
            msg = email.message_from_file(f)
        
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8", errors="replace")
        
        body = ""
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                charset = part.get_content_charset() or "utf-8"
                body += part.get_payload(decode=True).decode(charset, errors="replace")
        
        return subject, body
    except Exception as e:
        return None, f"Email processing error: {str(e)}"

@app.route("/", methods=["GET"])
def index():
    session.clear()  # Clear session on visiting home page
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return render_template("index.html", error="No file provided")
    
    file = request.files["file"]
    
    if file.filename == "":
        return render_template("index.html", error="No file selected")
    
    if not file.filename.endswith(".eml"):
        return render_template("index.html", error="Only .eml files are supported")
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)
    
    subject, body = extract_email_content(file_path)
    
    if not subject:
        return render_template("index.html", error=body)
    
    overview, explanation, score = analyze_with_groq(subject, body)
    
    # Store results in session
    session["filename"] = filename
    session["score"] = score
    session["overview"] = overview
    session["explanation"] = explanation
    
    return redirect(url_for("results"))

@app.route("/results")
def results():
    if "filename" not in session:
        return redirect(url_for("index"))  # Redirect to home if no session data
    return render_template(
        "index.html",
        filename=session.get("filename"),
        score=session.get("score"),
        overview=session.get("overview"),
        explanation=session.get("explanation"),
    )

@app.after_request
def add_header(response):
    """Ensure refresh always redirects to main page."""
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Expires"] = "0"
    return response

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
