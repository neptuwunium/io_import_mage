# SPDX-FileCopyrightText: 2026 Neptuwunium
#
# SPDX-License-Identifier: EUPL-1.2

from ctypes import BigEndianStructure, c_uint, c_ushort


class MNTNodeHeader(BigEndianStructure):
	_pack_ = 1
	_fields_ = [
		('index', c_ushort),
		('child_count', c_ushort),
		('child_index', c_ushort),
		('parent_index', c_ushort),
		('hash', c_uint),
		('name_offset', c_ushort),
		('group_id', c_ushort),
		('flags', c_uint),
	]


class MNTHeader(BigEndianStructure):
	_pack_ = 1
	_fields_ = [
		('magic', c_uint),
		('version_major', c_ushort),
		('version_minor', c_ushort),
		('size', c_uint),
		('count', c_ushort),
		('reserved', c_ushort),
		('flags', c_uint),
		('hash', c_uint),
		('hash_offset', c_uint),
		('id_offset', c_uint),
		('parent_offset', c_uint),
		('node_offset', c_uint),
		('child_offset', c_uint),
		('name_offset', c_uint),
	]
