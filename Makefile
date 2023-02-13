.PHONY: db run run-dev setup

db: 
	python db.py

run-dev: db
	python detect.py &
	python bot.py &

run:
	python detect.py &
	python bot.py &

setup:
	git clone https://github.com/ultralytics/yolov5
	pip install --upgrade pip
	pip install -r ./requirements.txt
	pip install -r ./yolov5/requirements.txt