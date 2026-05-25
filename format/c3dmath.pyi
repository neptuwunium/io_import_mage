# SPDX-FileCopyrightText: 2026 Neptuwunium
#
# SPDX-License-Identifier: EUPL-1.2

from ctypes import BigEndianStructure


class Vector2(BigEndianStructure):
	x: float
	y: float


class Vector3(BigEndianStructure):
	x: float
	y: float
	z: float


class Vector4(BigEndianStructure):
	x: float
	y: float
	z: float
	y: float
