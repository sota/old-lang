
PY = python
RPY = src/pypy/rpython/bin/rpython
PROGRAM = rffi
TARGET = targetrffi.py

rffi: src/cli/libcli.so targetrffi.py
	$(PY) -B $(RPY) --output $(PROGRAM) $(TARGET)

src/cli/libcli.so: submods
	(cd src/cli && make)

submods:
	git submodule update --init src/docopt
	git submodule update --init src/pypy

clean:
	(cd src/cli && make clean)
	git clean -xfd
