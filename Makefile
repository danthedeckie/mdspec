format:
	isort mdspec tests
	black mdspec tests

lint:
	isort --check-only mdspec tests
	black --diff mdspec tests

test:
	python3 -m unittest

test-repeat:
	watchfiles 'make test'

