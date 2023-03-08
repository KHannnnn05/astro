install:
	sudo apt-get install python3 python3-pip -y
	python3 -m pip install --upgrade pip
	python3 -m pip install --upgrade -r req.txt
	cd services && sudo mv * /etc/systemd/system/ && cd ..
	sudo systemctl daemon-reload
	sudo systemctl start fastapi.service
	sudo systemctl start parser.service
	sudo systemctl start parser.timer
	sudo enable fastapi.service
	sudo enable parser.service
	sudo enable parser.timer

start_server:
	uvicorn server:app --reload --host 0.0.0.0

start_parser:
	python3 main.py