# init_db.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, Voucher

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///local.db'
db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()

    # Insert test data
    vouchers = [
        Voucher(user_id='12345', voucher_url='https://eyeqcoach.com/activation?code=18724528-4e77-4e6f-81a0-7f8f816f233a'),
        Voucher(user_id='67890', voucher_url='https://eyeqcoach.com/activation?code=18724528-4e77-4e6f-81a0-7f8f816f233a')
    ]
    db.session.add_all(vouchers)
    db.session.commit()
