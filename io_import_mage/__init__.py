# SPDX-FileCopyrightText: 2026 Neptuwunium
#
# SPDX-License-Identifier: EUPL-1.2

bl_info = {
	'name': 'io_import_mage',
	'author': 'neptuwunium',
	'version': (1, 0, 0),
	'blender': (5, 1, 0),
	'location': 'File > Import > MAGE',
	'description': 'Import MAGE Actor',
	'warning': '',
	'tracker_url': 'https://github.com/neptuwunium/io_import_mage',
	'support': 'COMMUNITY',
	'category': 'Import-Export'
}

import io_import_mage.blender


def register(): io_import_mage.blender.register()


def unregister(): io_import_mage.blender.unregister()


if __name__ == '__main__':
	register()
