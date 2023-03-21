CARGO = cargo
MAKE = make
POETRY = poetry
PYTHON = $(POETRY) run python


.PHONY: help publish readme tokei uncache


help:
	@echo "make help:    Print help information"
	@echo "make publish: Build and upload the package to PyPi"
	@echo "make readme:  Get code statistics with Tokei"
	@echo "make tokei:   Build personal Tokei"
	@echo "make uncache: Remove __pycache__ directories"

publish:
	$(POETRY) build
	$(POETRY) publish

readme: tokei
	@$(PYTHON) script/readme/main.py

tokei:
	@cp script/readme/config/languages.json script/readme/tokei/
	@cd script/readme/tokei/ && $(CARGO) build --release

uncache:
	@$(PYTHON) -c "list(map(__import__('shutil').rmtree, __import__('pathlib').Path('.').rglob('__pycache__')))"
