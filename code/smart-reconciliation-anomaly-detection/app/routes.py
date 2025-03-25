from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os
from threading import Thread
from app.anomaly_detection import detect_anomalies
from app.email_notification import send_email_with_attachment

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Global variables to track processing status
is_processing = False
result_data = None


def process_uploaded_file(filepath):
    """Process uploaded file and run anomaly detection."""
    global is_processing, result_data
    try:
        # Load and analyze data
        df = pd.read_csv(filepath)
        result_data = detect_anomalies(df)

        # Convert the DataFrame to a list of dictionaries for rendering
        result_data = result_data.to_dict(orient="records")

        # Save the results
        pd.DataFrame(result_data).to_csv("anomaly_report.txt", index=False)
    finally:
        is_processing = False


@app.route("/", methods=["GET", "POST"])
def index():
    global is_processing, result_data

    if request.method == "POST":
        # If a file is uploaded, process it
        if "file" in request.files:
            file = request.files["file"]
            if file.filename != "":
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
                file.save(filepath)

                # Start analysis in a separate thread
                is_processing = True
                Thread(target=process_uploaded_file, args=(filepath,)).start()
                return redirect(url_for("status"))

    return render_template("dashboard.html", result_data=None, is_processing=False)


@app.route("/status")
def status():
    """Check the status of data processing."""
    global is_processing, result_data

    if is_processing:
        return render_template("dashboard.html", result_data=None, is_processing=True)

    # REMOVE or COMMENT THIS LINE
    # html_table = result_data.to_html(index=False, escape=False)

    # Pass result_data as list of dictionaries
    if result_data is not None:
        return render_template("dashboard.html", result_data=result_data, is_processing=False)

    return redirect(url_for("index"))



if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
