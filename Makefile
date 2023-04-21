requirements:
		pip install --upgrade pip
		pip install -r requirements.txt

env:
		echo "TOKEN=\nAPI_KEY=\nAPI_CUR_KEY=" > .env
		vim .env

run_bot:
		python ./bot/main.py
