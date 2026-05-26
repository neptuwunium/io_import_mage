# SPDX-FileCopyrightText: 2026 Neptuwunium
#
# SPDX-License-Identifier: EUPL-1.2

from ctypes import BigEndianStructure

from io_import_mage.format.structs.enums import KFMChannelStorage, KFMChannelTarget


class KFMFrameNode(BigEndianStructure):
	frame_count: int
	compress_bit_index: int
	frame_id_index: int
	value_offset: int


class KFMFrame(BigEndianStructure):
	magic: int
	frame_offset: int
	value_offset: int
	compress_offset: int


class KFMPtr(BigEndianStructure):
	size: int
	offset: int


class KFMNodeHeader(BigEndianStructure):
	hash: int
	id: int
	mnt_id: int
	_channel: int
	count: int
	id2: int
	frame_node_offset: int
	frame_node_count: int
	group_id: int
	flags: int
	reserved1: int
	reserved2: int
	reserved3: int

	@property
	def channel(self) -> KFMChannelStorage: pass

	@property
	def target(self) -> KFMChannelTarget: pass


class KFMHeader(BigEndianStructure):
	magic: int
	version_major: int
	version_minor: int
	flags: int
	header_size: int
	file_size: int
	frame_count: int
	const_count: int
	motion_count: int
	frame_info_count: int
	node_offset: int
	frame_count_offset: int
	frame_info_offset: int
	hash: int
	name_offset: int
	group_id: int
	group_flags: int
	offset: int
	node_size: int
