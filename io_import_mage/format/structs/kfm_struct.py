# SPDX-FileCopyrightText: 2026 Neptuwunium
#
# SPDX-License-Identifier: EUPL-1.2

from ctypes import BigEndianStructure, c_uint, c_int, c_byte, c_ushort

from io_import_mage.format.structs.enums import KFMChannel

class KFMFrameNode(BigEndianStructure):
	_pack_ = 1
	_fields_ = [
		('frame_count', c_ushort),
		('compress_bit_index', c_ushort),
		('frame_id_index', c_ushort),
		('value_index', c_ushort),
	]

class KFMFrame(BigEndianStructure):
	_pack_ = 1
	_fields_ = [
		('magic', c_ushort),
		('frame_offset', c_ushort),
		('value_offset', c_ushort),
		('compress_offset', c_ushort),
	]

class KFMPtr(BigEndianStructure):
	_pack_ = 1
	_fields_ = [
		('size', c_uint),
		('offset', c_uint),
	]

class KFMNode(BigEndianStructure):
	_pack_ = 1
	_fields_ = [
		('hash', c_uint),
		('id', c_ushort),
		('mnt_id', c_ushort),
		('_channel', c_byte),
		('count', c_byte),
		('id2', c_ushort),
		('frame_node_offset', c_ushort),
		('frame_node_count', c_ushort),
		('group_id', c_ushort),
		('flags', c_ushort),
		('reserved1', c_int),
		('reserved2', c_int),
		('reserved3', c_int),
	]

	@property
	def channel(self):
		return KFMChannel(self._channel)

class KFMHeader(BigEndianStructure):
	_pack_ = 1
	_fields_ = [
		('magic', c_uint),
		('version_major', c_byte),
		('version_minor', c_byte),
		('flags', c_ushort),
		('header_size', c_uint),
		('file_size', c_uint),
		('frame_count', c_ushort),
		('const_count', c_ushort),
		('motion_count', c_ushort),
		('frame_info_count', c_ushort),
		('node_offset', c_uint),
		('frame_count_offset', c_uint),
		('frame_info_offset', c_uint),
		('hash', c_uint),
		('name_offset', c_uint),
		('group_id', c_ushort),
		('group_flags', c_ushort),
		('offset', c_uint),
		('node_size', c_byte),
	]
