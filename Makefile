.PHONY: all clean list

# Directory for tarballs
TARBALL_DIR = tarballs

# Special directory that needs different handling
SPECIAL_DIR = kathara-lab_TP_Integrador

# Find all subdirectories (excluding tarballs dir, special dir, and hidden dirs)
SUBDIRS = $(shell ls -d */ | grep -v "$(TARBALL_DIR)/" | grep -v "$(SPECIAL_DIR)/" | grep -v "^\./")

# Default target - create all tarballs
all:
	mkdir -p $(TARBALL_DIR)
	@# Process regular directories
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
	@# Process special case for TP_Integrador directory
	@if [ -d "$(SPECIAL_DIR)" ]; then \
		for year in $$(ls -d $(SPECIAL_DIR)/*/ 2>/dev/null | xargs -n 1 basename); do \
			tarball="$(TARBALL_DIR)/$(SPECIAL_DIR)-$$year.tar.gz"; \
			yearpath="$(SPECIAL_DIR)/$$year"; \
			if [ ! -f "$$tarball" ] || [ "$$(find $$yearpath -type f -newer "$$tarball" 2>/dev/null | wc -l)" -gt 0 ]; then \
				echo "Creating $$tarball"; \
				tar -czf "$$tarball" "$$yearpath"; \
			else \
				echo "Skipping $$tarball (no changes)"; \
			fi; \
		done; \
	fi

# Remove all tarballs
clean:
	rm -rf $(TARBALL_DIR)

# Show directories to be compressed
list:
	@echo "Directories to be compressed:"
	@for dir in $(SUBDIRS); do \
		echo "  - $$(echo $$dir | sed 's|/$$||')"; \
	done
	@if [ -d "$(SPECIAL_DIR)" ]; then \
		echo "  - Special directory $(SPECIAL_DIR):"; \
		for year in $$(ls -d $(SPECIAL_DIR)/*/ 2>/dev/null | xargs -n 1 basename); do \
			echo "    - $(SPECIAL_DIR)/$$year → $(SPECIAL_DIR)-$$year.tar.gz"; \
		done; \
	fi