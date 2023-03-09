run:
	flask  run --debug

install:
	pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
	sudo apt install postgresql postgresql-contrib