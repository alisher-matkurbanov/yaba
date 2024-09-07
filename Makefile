.PHONY: run test-unit

run:
	uvicorn app.main:app --reload

test-unit:
	pytest
