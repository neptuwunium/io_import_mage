# SPDX-FileCopyrightText: 2026 Neptuwunium
#
# SPDX-License-Identifier: EUPL-1.2

from ctypes import BigEndianStructure, c_float


class Vector2(BigEndianStructure):
	_pack_ = 4
	_fields_ = [
		('x', c_float),
		('y', c_float),
	]


class Vector3(BigEndianStructure):
	_pack_ = 4
	_fields_ = [
		('x', c_float),
		('y', c_float),
		('z', c_float),
	]


class Vector4(BigEndianStructure):
	_pack_ = 4
	_fields_ = [
		('x', c_float),
		('y', c_float),
		('z', c_float),
	]
