CARGO = cargo
POETRY = poetry
PYTHON = $(POETRY) run python


.PHONY: help dev mypy publish pytest readme tokei uncache


help:
	@echo "make help:    Print help information"
	@echo "make dev:     Install the development dependencies"
	@echo "make mypy:    Check static type for Python"
	@echo "make publish: Build and upload the package to PyPi"
	@echo "make pytest:  Use pytest framework for unit testing"
	@echo "make readme:  Get code statistics with Tokei"
	@echo "make tokei:   Build personal Tokei"
	@echo "make uncache: Remove __pycache__ directories"

dev:
	@$(POETRY) install --extras full

mypy:
	@$(PYTHON) -m mypy --warn-unused-ignores iydon

publish:
	@$(POETRY) build
	@$(POETRY) publish

pytest:
	@$(PYTHON) -m pytest --pyargs iydon

readme: tokei
	@$(PYTHON) script/readme/main.py

tokei:
	@cp script/readme/config/languages.json script/readme/tokei/
	@cd script/readme/tokei/ && $(CARGO) build --release

uncache:
	@$(PYTHON) script/uncache.py
