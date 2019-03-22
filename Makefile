.SILENT:  # Ignore output of `echo` command


.PHONY: fmt  # Autoformat python files
fmt:
	@black src


.PHONY: up  # Run application service
up:
	@docker-compose up


.PHONY: test  # Run application service
test:
	@docker-compose run -e TESTING=true search pytest --cov=src


.PHONY: clean # Clean temp files from projects: .pyc. .pyo, __pycache__
clean:
	@find . \( -type d -name "__pycache__" -or -type f -name "*py[co]" \) -delete
	@echo "Python caching files has been deleted"
