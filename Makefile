venv:
		virtualenv venv
		source venv/bin/activate

requirements:
		pip install -r requirements.txt

env:
		touch .env
		vim .env

clean:
		rm -f Dockerfile docker-compose.yml README.md

run_bot:
		python ./bot/main.py
