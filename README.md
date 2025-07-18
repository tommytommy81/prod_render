my_redirect_app/
├── app_db.py               ← Flask app
├── models.py               ← SQLAlchemy models
├── requirements.txt
├── render.yaml             ← Render deployment config
├── .env (optional, ignored)
└── Procfile                ← Tells Render how to run the app



%% setting up the database

python init_db.py

sqlite3 instance/local.db .dump > migrate.sql

postgresql://redirect_db_twlc_user:z02xuAtWwIb9sAkCDBiLLWVYFCMH0LJx@dpg-d1rn917diees7393p6eg-a/redirect_db_twlc


make init         # (one-time setup)
make migrate      # create, dump, upload
make verify       # see what’s in the live DB
make all          # full run
