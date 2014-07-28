.PHONY: clean all launch launchcrunch test showlab

ASM := /usr/local/bin/acme
PUCRUNCH := /usr/local/bin/pucrunch
X64 := /Applications/Vice64/x64.app/Contents/MacOS/x64

BUILDDIR := build
LABELS := $(BUILDDIR)/labels.txt
GENCODE := $(BUILDDIR)/gen

TARGET_PRG := $(BUILDDIR)/vid64.prg
CRUNCH_PRG := $(BUILDDIR)/vid64cr.prg

VID := data/test.mov
SRCS := $(wildcard code/*.asm)

all: test $(TARGET_PRG) launch

$(TARGET_PRG): index.asm $(SRCS) $(GENCODE)/frame_init.asm $(GENCODE)/frames_delta.asm
	acme -l $(LABELS) $<

$(CRUNCH_PRG): $(TARGET_PRG)
	$(PUCRUNCH) $< $@

$(GENCODE)/frame_init.asm: $(VID)
	python gentools/initframe.py $< $@

$(GENCODE)/frames_delta.asm: $(VID)
	python gentools/deltaframes.py $< $@ 4 15

launch: $(TARGET_PRG)
	killall x64 || true
	$(X64) $< &

launchcrunch: $(CRUNCH_PRG)
	killall x64 || true
	$(X64) $< &

showlab: $(TARGET_PRG)
	cat $(LABELS)

clean:
	rm -f $(LABELS) $(TARGET_PRG)
	rm -f $(GENCODE)/frame_init.asm $(GENCODE)/frames_delta.asm

test:
	python gentools/vidextract/tests.py
