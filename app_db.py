from flask import Flask, redirect, abort
import os
import psycopg2

app = Flask(__name__)

# Database connection
def get_connection():
    return psycopg2.connect(os.environ['DATABASE_URL'])

@app.route('/<user_id>')
def redirect_user(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT voucher_url FROM vouchers WHERE user_id = %s", (user_id,))
    result = cur.fetchone()
    cur.close()
    conn.close()

    if result:
        return redirect(result[0])
    else:
        abort(404)

@app.route('/')
def index():
    return "Voucher Redirect Service is running!"

if __name__ == '__main__':
    app.run(debug=True)
