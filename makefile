RENDER_DB_URL=postgresql://redirect_db_twlc_user:z02xuAtWwIb9sAkCDBiLLWVYFCMH0LJx@dpg-d1rn917diees7393p6eg-a.oregon-postgres.render.com/redirect_db_twlc

export RENDER_DB_URL

init:
	pip install -r requirements.txt

migrate:
	python migrate_to_render.py

verify:
	psql "$(RENDER_DB_URL)?sslmode=require" -c 'SELECT * FROM vouchers;'

all: migrate verify
