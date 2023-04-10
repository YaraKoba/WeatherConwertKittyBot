venv:
		virtualenv venv

venv_act:
		source /usr/local/www/www9/para_kzn_bot/venv/bin/activate
requirements:
		pip install -r requirements.txt

env:
		touch .env
		vim .env

clean:
		rm -f Dockerfile docker-compose.yml README.md

run_bot:
		python ./bot/main.py

reminder:
		python ./bot/reminder.py
