.PHONY: install test fmt lint

install:
	uv sync

test:
	uv run pytest -v

fmt:
	uv run ruff format .
	uv run ruff check --fix .

lint:
	uv run ruff check .
