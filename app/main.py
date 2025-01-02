from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import boto3
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)

# S3 Configuration (using environment variables for AWS credentials)
S3_BUCKET = 'user-images-upload-harsha-02012024'
S3_REGION = 'ap-south-1'

# AWS credentials from environment variables
AWS_ACCESS_KEY_ID = os.getenv("AKIA4WJPWSWVIBPVY22V")
AWS_SECRET_ACCESS_KEY = os.getenv("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")

# Initialize S3 client with AWS credentials
s3 = boto3.client(
    's3',
    region_name=S3_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# Database Configuration (Assuming PostgreSQL is running inside Docker)
DB_HOST = "host.docker.internal"  # Update if you are using Docker's container name or IP
DB_NAME = "mydb"
DB_USER = "postgres"
DB_PASSWORD = "password"

# Connect to PostgreSQL
def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

# Set upload folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    email = request.form.get("email")
    image = request.files["image"]

    if not (name and email and image):
        return "All fields are required!", 400

    # Save image locally and upload to S3
    filename = secure_filename(image.filename)
    local_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(local_path)

    # Upload file to S3
    try:
        s3.upload_file(local_path, S3_BUCKET, filename)
        s3_url = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{filename}"
    except Exception as e:
        return f"Error uploading file: {str(e)}", 500

    # Save data to database
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, image_url, created_at) VALUES (%s, %s, %s, %s)",
            (name, email, s3_url, datetime.utcnow())
        )
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        return f"Error saving to database: {str(e)}", 500

    # Redirect to success page after successful form submission
    return render_template('success.html', name=name, s3_url=s3_url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
