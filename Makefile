install:
	sudo yum install python3 python3-pip -y
	python3 -m pip install --upgrade pip
	python3 -m pip install --upgrade -r req.txt

start_server:
	uvicorn server:app --reload --host 0.0.0.0

start_parser:
	python3 main.py
