# Face Recognition Attendance System

## Project Overview

The **Face Recognition Attendance System** is an innovative solution that leverages facial recognition technology to automate the attendance marking process. This system uses a webcam to capture real-time video feeds, detects faces, and marks attendance automatically when a registered face is detected. The system also includes a faculty login panel to allow instructors to manage and view attendance records date-wise. Email notifications are sent to the guardians of absent students after each class.

This system is built using Python, Flask, OpenCV, and face recognition technologies. It is designed to be easy to use, with a simple interface for both faculty and students.

## Features

- **Automatic Attendance Marking**: Attendance is marked when a registered face is detected.
- **Faculty Dashboard**: Faculty members can log in to view attendance records, delete specific attendance files, and monitor attendance over time.
- **Email Notifications**: After marking attendance, the system sends emails to the guardians of the students who were absent.
- **Faculty Login**: A secure login system for faculty members to access the attendance records.
- **Webcam Interface**: Real-time webcam feed to register student attendance.
- **Date-wise Attendance Records**: Attendance is stored date-wise in CSV files.

## Technologies Used

- **Flask**: Python web framework for building the web application.
- **Face Recognition**: A Python library for recognizing and manipulating faces.
- **OpenCV**: A library used for capturing video feeds from the webcam.
- **HTML/CSS**: For designing the user interface.
- **Python SMTP (Gmail)**: Used to send email notifications to guardians.
- **JavaScript**: For enhancing the frontend functionalities.

## Prerequisites

Before you run the project, ensure you have the following installed:

- **Python 3.7 or above**: Download and install Python from the [official website](https://www.python.org/downloads/).
- **Required Libraries**: All required libraries are listed in the `requirements.txt` file, which can be installed using `pip`.

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/Face_Recognition_Attendance.git
cd Face_Recognition_Attendance
```
## Installation

### Step 2: Set Up the Virtual Environment

- For **Windows**:
    ```
    python -m venv venv
    venv\Scripts\activate
    ```

- For **macOS/Linux**:
    ```
    python3 -m venv venv
    source venv/bin/activate
    ```

### Step 3: Install Dependencies

Once the virtual environment is activated, install the required libraries:
```
pip install -r requirements.txt
```
###Step 4: Prepare Student Images
Place the student images in the student_photos/ directory. Ensure that the images are named appropriately for the student.

###Step 5: Run the Application
Start the Flask server by running the command:
```
python attendance_dashboard.py
```
## Contact

If you have any questions or need further assistance, feel free to reach out to hemanthmg1406@gmail.com.







