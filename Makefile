.PHONY: clean all launch test

ASM := /usr/local/bin/acme
# PUCRUNCH := /usr/local/bin/pucrunch
X64 := /Applications/Vice64/x64.app/Contents/MacOS/x64

BUILDDIR := build
LABELS := $(BUILDDIR)/labels
GENCODE := $(BUILDDIR)/gen

TARGET_PRG := $(BUILDDIR)/vid64.prg
VID := data/test.mov
SRCS := $(wildcard code/*.asm)

all: test $(TARGET_PRG) launch

$(TARGET_PRG): index.asm $(SRCS) $(GENCODE)/frame_init.asm
	acme -l $(LABELS) $<

$(GENCODE)/frame_init.asm: $(VID)
	python gentools/initframe.py $< $@

launch: $(TARGET_PRG)
	killall x64 || true
	$(X64) $< &

clean:
	rm -f $(LABELS) $(TARGET_PRG) $(GENCODE)/frame_init.asm

test:
	python gentools/vidextract/tests.py
