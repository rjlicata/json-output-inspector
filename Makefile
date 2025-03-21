DATA?="${PWD}"
DOCKER_FILE=Dockerfile
NAME?=llm-json
WORKING_DIR=/workspace
CURRENT_UID := $(shell id -u)
CURRENT_GID := $(shell id -g)

build:
	docker build -t $(NAME) -f $(DOCKER_FILE) .

bash: build
	docker run -it --net=host --rm  -w $(WORKING_DIR) --shm-size=10.07gb -v $(DATA):/workspace $(NAME) /bin/bash
