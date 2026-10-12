.PHONY: data tests lint format help

pipeline: tests data validate ## Run the full pipeline
	@echo "Done..."

data: ## Convert data files
	uv run python -m data.convert

validate: ## Run data validation rules
	uv run python -m data.validation

tests: ## Run tests
	uv run --extra dev pytest

lint: ## Run linters
	uv run --extra dev,notebook isort --check-only src notebooks
	uv run --extra dev,notebook black --check src notebooks

format: ## Format the code
	uv run --extra dev,notebook isort src notebooks
	uv run --extra dev,notebook black src notebooks

help: ## Display this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
