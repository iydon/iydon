CARGO = cargo
MAKE = make
POETRY = poetry
PYTHON = $(POETRY) run python


.PHONY: help readme tokei


help:
	@echo "make help:   Print help information"
	@echo "make readme: Get code statistics with Tokei"
	@echo "make tokei:  Build personal Tokei"

readme: tokei
	@$(PYTHON) script/readme/main.py

tokei:
	@cp script/readme/config/languages.json script/readme/tokei/
	@cd script/readme/tokei/ && $(CARGO) build --release
