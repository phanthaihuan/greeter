.PHONY: setup compile server client stop run clean
SHELL := /bin/zsh
VENV := venv
PIP := $(VENV)/bin/pip
PYTHON := $(VENV)/bin/python
SCRIPT_SERVER := greeter_server.py
SCRIPT_CLIENT := greeter_client.py
PID_FILE := server.pid

setup:
	@echo "Setting up the project..."
	@echo "Setup virtual environment..."
	python3 -m venv $(VENV)
	@echo "Installing required packages..."
	$(PIP) install grpcio grpcio-tools protobuf
	@echo "Project setup complete."

compile: setup
	@echo "Compiling greet.proto to generate gRPC code..."
	$(PYTHON) -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. greet.proto
	@echo "Compilation complete."

server: compile
	@echo "Start the server..."
	$(PYTHON) $(SCRIPT_SERVER) & echo $$! > $(PID_FILE)

client:
	@echo "Start the client..."
	$(PYTHON) $(SCRIPT_CLIENT)

run: server client
	@echo "Running for testing completed. You can run 'make stop' now."

stop:
	@if [ -f $(PID_FILE) ]; then \
	    PID=`cat $(PID_FILE)`; \
	    echo "🛑 Stopping server with PID $$PID..."; \
	    kill $$PID; \
	    rm $(PID_FILE); \
	else \
	    echo "⚠️ Server PID file not found. Is the server running?"; \
	fi

clean:
	@echo "🧹 Cleaning up..."
	@rm -rf $(VENV)
	@rm -f greet_pb2.py greet_pb2_grpc.py
	@rm -f $(PID_FILE)
	@echo "✅ Cleanup complete."
