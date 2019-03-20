.SILENT:  # Ignore output of make `echo` command


.PHONY: fmt  # Autoformat python files
fmt:
	@black src


.PHONY: up  # Run application service
up:
	@docker-compose up

