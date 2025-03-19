.PHONY: all clean list

# Directory for tarballs
TARBALL_DIR = tarballs

# Find all subdirectories (excluding tarballs dir and hidden dirs)
SUBDIRS = $(shell ls -d */ | grep -v "$(TARBALL_DIR)/" | grep -v "^\./")

# Default target - create all tarballs
all:
	mkdir -p $(TARBALL_DIR)
	@for dir in $(SUBDIRS); do \
	dirname=$$(echo $$dir | sed 's|/$$||'); \
	tarball="$(TARBALL_DIR)/$$dirname.tar.gz"; \
	if [ ! -f "$$tarball" ] || [ "$$(find $$dirname -type f -newer "$$tarball" 2>/dev/null | wc -l)" -gt 0 ]; then \
	echo "Creating $$tarball"; \
	tar -czf "$$tarball" "$$dirname"; \
else \
	echo "Skipping $$tarball (no changes)"; \
	fi; \
	done

# Remove all tarballs
clean:
	rm -rf $(TARBALL_DIR)

# Show directories to be compressed
list:
	@echo "Directories to be compressed:"
	@for dir in $(SUBDIRS); do \
	echo "  - $$(echo $$dir | sed 's|/$$||')"; \
	done