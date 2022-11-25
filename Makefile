POETRY = poetry
PYTHON = $(POETRY) run python
TOKEI = tokei


.PHONY: help stats tokei version


help:
	@echo "make help:    Print help information"
	@echo "make stats:   Get code statistics with Tokei"
	@echo "make tokei:   Count my code, quickly"
	@echo "make version: Update version number in configuration(s)"

stats:
	@$(PYTHON) script/code_statistics/main.py

tokei:
	@$(TOKEI) script/code_statistics/cache/

version:
	@$(PYTHON) script/version.py
