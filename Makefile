# Sourdough Science - build targets
# Markdown under docs/ is the source of truth.

CHAPTERS := $(sort $(wildcard docs/*.md))
BUILD    := build
TITLE    := Sourdough Science
SUBTITLE := Preferments, Fermentation Science, and Application

PANDOC_COMMON := --toc --toc-depth=2 --standalone \
                 --metadata title="$(TITLE)" \
                 --metadata subtitle="$(SUBTITLE)" \
                 --from=markdown+pipe_tables+yaml_metadata_block

.PHONY: all pdf docx html single clean list

all: pdf

$(BUILD):
	@mkdir -p $(BUILD)

single: | $(BUILD)
	@pandoc $(CHAPTERS) --from=markdown --to=markdown --standalone \
	  --metadata title="$(TITLE)" -o $(BUILD)/sourdough-science.md
	@echo "-> $(BUILD)/sourdough-science.md"

pdf: | $(BUILD)
	@pandoc $(CHAPTERS) $(PANDOC_COMMON) \
	  --pdf-engine=xelatex --template=templates/latex.tex \
	  -V geometry:margin=2.5cm \
	  -V fontsize=11pt \
	  -V linkcolor=black \
	  -V mainfont="DejaVu Serif" \
	  -V monofont="DejaVu Sans Mono" \
	  -o $(BUILD)/sourdough-science.pdf
	@echo "-> $(BUILD)/sourdough-science.pdf"

docx: | $(BUILD)
	@pandoc $(CHAPTERS) $(PANDOC_COMMON) -o $(BUILD)/sourdough-science.docx
	@echo "-> $(BUILD)/sourdough-science.docx"

html: | $(BUILD)
	@pandoc $(CHAPTERS) $(PANDOC_COMMON) --embed-resources \
	  -o $(BUILD)/sourdough-science.html
	@echo "-> $(BUILD)/sourdough-science.html"

list:
	@for f in $(CHAPTERS); do head -1 $$f | sed "s|^# |  |" ; done

clean:
	@rm -rf $(BUILD)
