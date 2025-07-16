from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Voucher(db.Model):
    user_id = db.Column(db.String, primary_key=True)
    voucher_url = db.Column(db.String, nullable=False)
