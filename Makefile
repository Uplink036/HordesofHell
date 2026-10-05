.PHONY: tests lint format help

tests: ## Run tests
	uv run --extra dev pytest

lint: ## Run linters
	isort --check-only source
	black --check source

format: ## Format the code
	isort source
	black source

help: ## Display this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
