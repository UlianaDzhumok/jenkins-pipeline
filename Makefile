setup:
	python3 -m venv ~/.jenkins-pipeline
	. ~/.jenkins-pipeline/bin/activate

install:
	# This should be run from inside a virtualenv
	pip3 install --upgrade pip &&\
		pip3 install -r requirements.txt
	sudo -S wget -O /bin/hadolint https://github.com/hadolint/hadolint/releases/download/v1.16.3/hadolint-Linux-x86_64
	sudo -S chmod +x /bin/hadolint

test-func:
	# Additional, optional, tests could go here
	python3 app.py --dir test_data/functional/
	
test-perf:
	# Additional, optional, tests could go here
	python3 app.py --dir test_data/performance/

lint:
	# See local hadolint install instructions:   https://github.com/hadolint/hadolint
	# This is linter for Dockerfiles
	hadolint Dockerfile
	
	# This is a linter for Python source code linter: https://www.pylint.org/
	# This should be run from inside a virtualenv
	pylint --disable=R,C,W1203,W1309,E0401,W0622 app.py

all: install lint test-func test-perf

