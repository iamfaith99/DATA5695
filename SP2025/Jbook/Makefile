# Makefile for building Jupyter Book PDF

# Default target
all: pdf

# Build PDF using jupyter-book
pdf:
	jb build --builder pdflatex jnotes/

# Clean build artifacts (optional but recommended)
clean:
	rm -rf jnotes/_build/

# Help command to show available targets
help:
	@echo "Available targets:"
	@echo "  make        - Build PDF (same as 'make pdf')"
	@echo "  make pdf    - Build PDF using jupyter-book"
	@echo "  make clean  - Remove build artifacts"
