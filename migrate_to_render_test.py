import os
import sqlite3
import subprocess
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# === Configuration ===
RENDER_DB_URL = os.getenv("RENDER_DB_URL")  # Set this as an environment variable or paste below
LOCAL_DB = "local.db"
DUMP_FILE = "migrate.sql"

# === Step 1: Create and populate local.db ===
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{LOCAL_DB}"
db = SQLAlchemy(app)

class Voucher(db.Model):
    __tablename__ = "vouchers"
    user_id = db.Column(db.String, primary_key=True)
    voucher_url = db.Column(db.String, nullable=False)

with app.app_context():
    db.drop_all()
    db.create_all()

    db.session.add_all([
        Voucher(user_id='12345', voucher_url='https://eyeqcoach.com/activation?code=18724528-4e77-4e6f-81a0-7f8f816f233a'),
        Voucher(user_id='67890', voucher_url='https://eyeqcoach.com/activation?code=18724528-4e77-4e6f-81a0-7f8f816f233a'),
   ])
    db.session.commit()
    print("✅ Local SQLite database created and populated.")

# === Step 2: Dump to migrate.sql ===
subprocess.run(["sqlite3", LOCAL_DB, ".dump"], stdout=open(DUMP_FILE, "w"))
print("✅ migrate.sql generated.")

# === Step 3: Clean migrate.sql for PostgreSQL ===
with open(DUMP_FILE, "r") as f:
    lines = f.readlines()

cleaned = []
for line in lines:
    if any(skip in line for skip in ("PRAGMA", "sqlite_sequence", "BEGIN", "COMMIT")):
        continue
    cleaned.append(line.replace("AUTOINCREMENT", ""))  # Remove SQLite-specific keywords

with open(DUMP_FILE, "w") as f:
    f.writelines(cleaned)

print("✅ migrate.sql cleaned for PostgreSQL.")

# === Step 4: Upload to Render PostgreSQL ===
if not RENDER_DB_URL:
    RENDER_DB_URL = input("🔐 Enter your Render PostgreSQL connection string: ")

print("☁️ Uploading migrate.sql to Render...")
subprocess.run(["psql", RENDER_DB_URL + "?sslmode=require", "-f", DUMP_FILE])
print("✅ Upload complete!")
