# SPDX-FileCopyrightText: 2026 Neptuwunium
#
# SPDX-License-Identifier: EUPL-1.2

from ctypes import BigEndianStructure

class MAGEHeader(BigEndianStructure):
	magic: int
	version_major: int
	version_minor: int
	version_patch: int
	is_big: bool
	table_offset: int
	count: int
	alignment: int
	type_id: int
	game_id: int
	name_length: int


class MAGEPtr(BigEndianStructure):
	offset: int
	size: int