all: deps

deps:
	./install_deps.sh
	touch deps

test: deps
	./run_tests.sh

clean:
	rm -rf deps

.PHONY: all test clean
