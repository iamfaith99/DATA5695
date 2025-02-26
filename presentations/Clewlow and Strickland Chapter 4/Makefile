# Variables
QMD_FILE = clewlow_strickland_chap4.qmd
OUTPUT_FILE = clewlow_strickland_chap4.html
QUARTO_CMD = quarto

# Default target
all: render

# Render the presentation
render: $(QMD_FILE)
	$(QUARTO_CMD) render $(QMD_FILE)

# Clean up generated files
clean:
	rm -f $(OUTPUT_FILE)

# View the presentation in a browser
view: $(OUTPUT_FILE)
	open $(OUTPUT_FILE)

# Rebuild the presentation (clean and render)
rebuild: clean render

# Help target to list available commands
help:
	@echo "Makefile for Quarto Presentation"
	@echo "Usage:"
	@echo "  make render   - Render the presentation"
	@echo "  make clean    - Remove the rendered output"
	@echo "  make view     - Open the presentation in a browser"
	@echo "  make rebuild  - Clean and render the presentation"