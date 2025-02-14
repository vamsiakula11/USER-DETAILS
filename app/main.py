from flask import Flask, render_template, request
import psycopg2
import os
import boto3
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)

# Database Configuration (PostgreSQL)
DB_HOST = "database-1.c9scia20gbq0.ap-south-1.rds.amazonaws.com"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "Allvy1234"

# S3 Configuration
S3_BUCKET = "new-one-01"
S3_REGION = "ap-south-1"  # Change this to your AWS region
AWS_ACCESS_KEY = "AKIASDRANKCOTO7VAKB5"
AWS_SECRET_KEY = "FgPrAsxPsHQEqAfe30lEW2+6yUN/bsHZNs98yw+T"

# Initialize S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=S3_REGION
)

# Connect to PostgreSQL
def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    email = request.form.get("email")
    image = request.files.get("image")

    if not (name and email):
        return "Name and email are required!", 400

    image_url = None  # Default to None if no image is uploaded

    if image:
        filename = secure_filename(image.filename)
        s3_key = f"uploads/{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{filename}"

        try:
            # Upload image to S3
            s3.upload_fileobj(image, S3_BUCKET, s3_key)
            image_url = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{s3_key}"
        except Exception as e:
            return f"Error uploading file to S3: {str(e)}", 500

    # Save data to database with S3 image URL
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, image_url, created_at) VALUES (%s, %s, %s, %s)",
            (name, email, image_url, datetime.utcnow())
        )
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        return f"Error saving to database: {str(e)}", 500

    return render_template('success.html', name=name, image_url=image_url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
