# SPDX-FileCopyrightText: 2026 Neptuwunium
#
# SPDX-License-Identifier: EUPL-1.2

from ctypes import BigEndianStructure, c_uint, c_int, c_ushort

class MOPHeader(BigEndianStructure):
	_pack_ = 1
	_fields_ = [
		('magic', c_uint),
		('version_major', c_ushort),
		('version_minor', c_ushort),
		('header_size', c_uint),
		('file_size', c_uint),
		('count', c_int),
		('size_offset', c_int),
		('anim_offset', c_int),
		('name_offset', c_int),
	]
