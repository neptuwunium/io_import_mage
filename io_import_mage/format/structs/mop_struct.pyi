# SPDX-FileCopyrightText: 2026 Neptuwunium
#
# SPDX-License-Identifier: EUPL-1.2

from ctypes import BigEndianStructure


class MOPHeader(BigEndianStructure):
	magic: int
	version_major: int
	version_minor: int
	header_size: int
	file_size: int
	count: int
	size_offset: int
	anim_offset: int
	name_offset: int
