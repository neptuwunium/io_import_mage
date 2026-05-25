# SPDX-FileCopyrightText: 2026 Neptuwunium
#
# SPDX-License-Identifier: EUPL-1.2

from ctypes import BigEndianStructure


class MNTNodeHeader(BigEndianStructure):
	index: int
	child_count: int
	child_index: int
	parent_index: int
	hash: int
	name_offset: int
	group_id: int
	flags: int


class MNTHeader(BigEndianStructure):
	magic: int
	version_major: int
	version_minor: int
	size: int
	count: int
	reserved: int
	flags: int
	hash: int
	hash_offset: int
	id_offset: int
	parent_offset: int
	node_offset: int
	child_offset: int
	name_offset: int
