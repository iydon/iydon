CARGO = cargo
POETRY = poetry
PYTHON = $(POETRY) run python


.PHONY: help dev mkdocs mypy nox publish pytest readme tokei uncache upgrade


help:
	@echo "make help:    Print help information"
	@echo "make dev:     Install the development dependencies"
	@echo "make mkdocs:  Build the MkDocs documentation"
	@echo "make mypy:    Check static type for Python"
	@echo "make nox:     Use nox for automate and standardize testing"
	@echo "make publish: Build and upload the package to PyPi"
	@echo "make pytest:  Use pytest framework for unit testing"
	@echo "make readme:  Get code statistics with Tokei"
	@echo "make tokei:   Build personal Tokei"
	@echo "make uncache: Remove __pycache__ directories"
	@echo "make upgrade: Bump semantic version (simple)"

dev:
	@$(POETRY) install --extras full

mkdocs:
	@$(PYTHON) -m mkdocs build

mypy:
	@$(PYTHON) -m mypy --warn-unused-ignores iydon

nox:
	@cp script/noxfile.py .
	@$(PYTHON) -m nox
	@rm noxfile.py

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

upgrade:
	@$(PYTHON) script/upgrade.py
