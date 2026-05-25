# SPDX-FileCopyrightText: 2026 Neptuwunium
#
# SPDX-License-Identifier: EUPL-1.2

BLENDER = blender

.PHONY: dirs build clean

build: dirs
	$(BLENDER) --command extension build --source-dir io_import_mage --output-dir build

dirs:
	mkdir -p build

clean:
	rm build/io_import_mage-*.zip

all: build