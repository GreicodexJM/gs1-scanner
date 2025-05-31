# Makefile for building, dockerizing, pushing, and deploying the hash-logo-generator

IMAGE_NAME = greicodex/gs1
COMMIT_ID = $(shell git rev-parse --short HEAD)
K8S_FILE = k8s-serverless.yaml

.PHONY: all docker-build docker-push k8s-update k8s-apply deploy

all: deploy

# Build the Docker image tagged with the current commit id
docker-build: 
	@echo "Building Docker image with tag: $(COMMIT_ID)"
	docker build -t $(IMAGE_NAME):$(COMMIT_ID) .

# Push the Docker image to Docker Hub
docker-push: docker-build
	@echo "Pushing Docker image: $(IMAGE_NAME):$(COMMIT_ID)"
	docker push $(IMAGE_NAME):$(COMMIT_ID)

# Update the image tag in the Kubernetes YAML file
k8s-update:
	@echo "Updating image tag in $(K8S_FILE) to $(COMMIT_ID)"
	# Use sed to replace the image tag in the k8s file
	sed -i.bak -E "s|(image: $(IMAGE_NAME):)[^[:space:]]+|\1$(COMMIT_ID)|" $(K8S_FILE)

# Apply the Kubernetes configuration
k8s-apply:
	@echo "Applying Kubernetes configuration from $(K8S_FILE)"
	kubectl apply -f $(K8S_FILE)

# Full deploy: build, docker build, push, update k8s file, and apply
deploy: docker-push k8s-update k8s-apply
	@echo "Deployment complete with image tag: $(COMMIT_ID)"
