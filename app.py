from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "secret123"

# Folder to save uploaded resumes
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 30 * 1024 * 1024  # 30 MB max size

# Allowed file extensions
ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get form fields
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        country_code = request.form.get("country_code")
        gender = request.form.get("gender")
        dob = request.form.get("dob")
        resume = request.files.get("resume")

        # Validation
        if not name or not email or not phone or not gender or not dob or not resume:
            flash("All fields are required!", "danger")
            return redirect(request.url)

        if resume and allowed_file(resume.filename):
            filename = secure_filename(resume.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            resume.save(filepath)

            flash("Application submitted successfully!", "success")
            return redirect(request.url)
        else:
            flash("Invalid file format! Only PDF, DOC, DOCX allowed.", "danger")
            return redirect(request.url)

    return render_template("form.html")

if __name__ == "__main__":
    app.run(debug=True)

