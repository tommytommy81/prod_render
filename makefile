RENDER_DB_URL =

export RENDER_DB_URL

init:
	pip install -r requirements.txt

migrate:
	python migrate_to_render.py

verify:
	psql "$(RENDER_DB_URL)?sslmode=require" -c 'SELECT * FROM vouchers;'

all: migrate verify
