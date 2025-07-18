# migrate_to_render.py

import os
import csv
import sqlite3
import subprocess
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# === CONFIG ===
RENDER_DB_URL = os.getenv("RENDER_DB_URL")  # or prompt
LOCAL_DB = "local.db"
DUMP_FILE = "migrate.sql"
CSV_FILE = "vouchers.csv"

# === Set up Flask app and DB ===
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{LOCAL_DB}"
db = SQLAlchemy(app)

class Voucher(db.Model):
    __tablename__ = "vouchers"
    user_id = db.Column(db.String, primary_key=True)
    voucher_url = db.Column(db.String, nullable=False)

def create_and_populate_db():
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Read from CSV
        with open(CSV_FILE, newline='') as f:
            reader = csv.DictReader(f)
            entries = [Voucher(user_id=row['user_id'], voucher_url=row['voucher_url']) for row in reader]
            db.session.add_all(entries)
            db.session.commit()

    print("✅ local.db created and populated from CSV.")

def export_sqlite():
    subprocess.run(["sqlite3", LOCAL_DB, ".dump"], stdout=open(DUMP_FILE, "w"))
    print("✅ migrate.sql generated.")

    # Clean SQL
    with open(DUMP_FILE, "r") as f:
        lines = f.readlines()

    cleaned = []
    for line in lines:
        if any(skip in line for skip in ("PRAGMA", "sqlite_sequence", "BEGIN", "COMMIT")):
            continue
        cleaned.append(line.replace("AUTOINCREMENT", ""))

    with open(DUMP_FILE, "w") as f:
        f.writelines(cleaned)

    print("✅ migrate.sql cleaned for PostgreSQL.")

def upload_to_render():
    global RENDER_DB_URL
    if not RENDER_DB_URL:
        RENDER_DB_URL = input("🔐 Enter your Render PostgreSQL connection string: ")

    print("☁️ Uploading migrate.sql to Render...")
    subprocess.run(["psql", RENDER_DB_URL + "?sslmode=require", "-f", DUMP_FILE])
    print("✅ Upload complete.")

def verify_upload():
    print("🔍 Verifying data in Render DB...")
    result = subprocess.run(
        ["psql", RENDER_DB_URL + "?sslmode=require", "-c", "SELECT * FROM vouchers;"],
        capture_output=True, text=True
    )
    print(result.stdout)

if __name__ == "__main__":
    create_and_populate_db()
    export_sqlite()
    upload_to_render()
    verify_upload()
