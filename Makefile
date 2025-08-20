lint:
	flake8 .

openapi-sdk:
	openapi-generator-cli generate -i http://localhost:8000/openapi.json -g python -o sdk/python

security-scan:
	bandit -r .

docker-scan:
	trivy image fastapi-demo || true
