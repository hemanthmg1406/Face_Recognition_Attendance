from flask import Flask, render_template, Response, redirect, url_for, request, session, flash
import cv2
import face_recognition
import numpy as np
import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from threading import Timer
import webbrowser

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Global variables
known_faces = []
known_names = []
attendance_log = {}
student_photos_path = "student_photos"
attendance_folder = "attendance_files"
today_date = datetime.now().strftime("%Y-%m-%d")
attendance_file = f"{attendance_folder}/attendance_{today_date}.csv"
is_webcam_running = False
attendance_message = ""

# Email configuration
sender_email = "hem.hemanthkumar1406@gmail.com"
sender_password = "psdn gvgz gnja ttnn"
smtp_server = "smtp.gmail.com"
smtp_port = 465
guardian_emails = {
    "Dineshkumar": "ahzlguwlw@10mail.org",
    "Gokul": "skhtvojtj@emltmp.com",
    "Kishorekumar": "jyz0nalemal3@10mail.xyz",
    "Manoj": "ahodffiof@yomail.info",
    "Methunkumar": "hemanthmg1406@gmail.com"
}

# Ensure attendance folder exists
os.makedirs(attendance_folder, exist_ok=True)

# Load known faces
def load_known_faces():
    global known_faces, known_names
    for file in os.listdir(student_photos_path):
        if file.endswith(('.jpg', '.jpeg', '.png')):
            name, _ = os.path.splitext(file)
            image_path = os.path.join(student_photos_path, file)
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_faces.append(encodings[0])
                known_names.append(name)

# Mark attendance
def mark_attendance(student_name):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if student_name not in attendance_log:
        attendance_log[student_name] = timestamp
        with open(attendance_file, "a") as file:
            file.write(f"{student_name},{timestamp},Present\n")

# Send email notifications
def send_email_notifications():
    absent_students = set(known_names) - set(attendance_log.keys())
    for student in absent_students:
        if student in guardian_emails:
            email = guardian_emails[student]
            subject = f"Attendance Notification: Your Ward is Absent on {today_date}"
            body = f"""Dear Guardian,

This is to inform you that your ward, {student}, was absent for the class on {today_date}.

Thank you,
School Administration"""
            send_email(email, subject, body)

# Send email
def send_email(to_email, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
        print(f"Email sent to {to_email}.")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")

# Video feed generator
def gen_frames():
    global is_webcam_running, attendance_message
    video_capture = cv2.VideoCapture(0)
    while is_webcam_running:
        success, frame = video_capture.read()
        if not success:
            break
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_faces, face_encoding)
            face_distances = face_recognition.face_distance(known_faces, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_names[best_match_index]
                mark_attendance(name)
                attendance_message = f"YOUR ATTENDANCE IS REGISTERED: {name}"
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    video_capture.release()

# Login required decorator
def login_required(f):
    def wrap(*args, **kwargs):
        if "logged_in" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

# Routes
@app.route("/")
def index():
    return render_template("attendance_dashboard.html", message=attendance_message)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "faculty" and password == "faculty123":
            session["logged_in"] = True
            return redirect(url_for("faculty_dashboard"))
        else:
            flash("Invalid credentials!", "error")
    return render_template("attendance_dashboard.html")

@app.route("/faculty_dashboard", methods=["GET", "POST"])
@login_required
def faculty_dashboard():
    attendance_files = sorted(os.listdir(attendance_folder))
    if request.method == "POST":
        file_to_delete = request.form.get("file_to_delete")
        os.remove(os.path.join(attendance_folder, file_to_delete))
        flash(f"Deleted file: {file_to_delete}", "info")
        return redirect(url_for("faculty_dashboard"))
    return render_template("faculty_dashboard.html", attendance_files=attendance_files)

@app.route("/video_feed")
def video_feed():
    return Response(gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/start_webcam")
def start_webcam():
    global is_webcam_running
    is_webcam_running = True
    return redirect(url_for("index"))

@app.route("/end_webcam")
def end_webcam():
    global is_webcam_running
    is_webcam_running = False
    send_email_notifications()
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    load_known_faces()
    Timer(1, lambda: webbrowser.open("http://127.0.0.1:5000")).start()
    app.run(debug=True)
