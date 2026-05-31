# SPDX-FileCopyrightText: 2026 Neptuwunium
#
# SPDX-License-Identifier: EUPL-1.2

bl_info = {
	'name': 'io_import_mage',
	'author': 'neptuwunium',
	'version': (1, 0, 4),
	'blender': (4, 5, 0),
	'location': 'File > Import > MAGE',
	'description': 'Import MAGE Actor',
	'warning': '',
	'tracker_url': 'https://github.com/neptuwunium/io_import_mage',
	'support': 'COMMUNITY',
	'category': 'Import-Export'
}

from . import blender


def register(): blender.register()


def unregister(): blender.unregister()


if __name__ == '__main__':
	register()
