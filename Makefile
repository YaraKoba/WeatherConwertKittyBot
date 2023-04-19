requirements:
		pip install --upgrade pip
		pip install -r requirements.txt

env:
		echo "TOKEN=\nAPI_KEY=\nADMIN_LOGIN=\nADMIN_PASSWORD=" > .env
		vim .env

run_bot:
		python ./bot/main.py
