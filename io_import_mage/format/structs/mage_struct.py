# SPDX-FileCopyrightText: 2026 Neptuwunium
#
# SPDX-License-Identifier: EUPL-1.2

from ctypes import LittleEndianStructure, c_uint, c_int, c_bool, c_byte


class MAGEHeader(LittleEndianStructure):
	_pack_ = 1
	_fields_ = [
		('magic', c_uint),
		('version_major', c_byte),
		('version_minor', c_byte),
		('version_patch', c_byte),
		('is_big', c_bool),
		('table_offset', c_uint),
		('count', c_int),
		('alignment', c_int),
		('type_id', c_uint),
		('game_id', c_uint),
		('name_length', c_uint),
	]


class MAGEPtr(LittleEndianStructure):
	_pack_ = 1
	_fields_ = [
		('offset', c_uint),
		('size', c_uint),
	]
