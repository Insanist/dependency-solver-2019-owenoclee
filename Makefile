all: compile

compile: deps

deps:
	./install_deps.sh
	touch deps

test: compile
	./run_tests.sh

clean:
	rm -rf deps

reallyclean: clean

.PHONY: all compile test clean reallyclean
