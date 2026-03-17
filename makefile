build:
	docker build -t pit-wall:latest .

dev: build
	docker run \
		-p 3000:3000 \
		-v ./main.py:/app/main.py \
		-v ./src:/app/src \
		--rm \
		pit-wall:latest

dev-shell: build
	docker run \
		-p 3000:3000 \
		--rm \
		-v ./main.py:/app/main.py \
		-v ./src:/app/src \
		-it \
		pit-wall:latest \
		bash
