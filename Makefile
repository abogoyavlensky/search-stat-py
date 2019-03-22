.SILENT:  # Ignore output of `echo` command


.PHONY: test  # Run application service
test:
	@TESTING=true pytest --cov=src


.PHONY: fmt  # Autoformat python files
fmt:
	@black src tests


.PHONY: clean # Clean temp files from projects: .pyc. .pyo, __pycache__
clean:
	@find . \( -type d -name "__pycache__" -or -type f -name "*py[co]" \) -delete
	@echo "Python caching files has been deleted"
