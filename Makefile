CARGO = cargo
MAKE = make
POETRY = poetry
PYTHON = $(POETRY) run python
TOKEI = ./script/tokei/target/release/tokei


.PHONY: help stats tokei tokei-build version


help:
	@echo "make help:        Print help information"
	@echo "make stats:       Get code statistics with Tokei"
	@echo "make tokei:       Count my code, quickly"
	@echo "make tokei-build: Build personal Tokei"
	@echo "make version:     Update version number in configuration(s)"

stats:
	@$(PYTHON) script/code_statistics/main.py
	@$(MAKE) tokei

tokei:
	@$(TOKEI) script/code_statistics/cache/ --num-format commas

tokei-build:
	@cd script/tokei && $(CARGO) build --release

version:
	@$(PYTHON) script/version.py
