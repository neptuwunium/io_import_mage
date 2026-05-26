# SPDX-FileCopyrightText: 2026 Neptuwunium
#
# SPDX-License-Identifier: EUPL-1.2
import enum
from enum import Enum


class KFMChannelStorage(Enum):
	FLOAT32 = 0x0  # size 4
	VEC2F = 0x1  # size 4 (2 elements)
	VEC3F = 0x2  # size 4 (3 elements)
	VEC4F = 0x3  # size 4 (4 elements)
	SCALE32 = 0x4  # size 4 (3 elements)
	TRANSLATION32 = 0x5  # size 4 (3 elements)
	ROTATION_RADIANS = 0x6  # size 4 (4 elements)
	ROTATION32W = 0x7  # size 4 (4 elements)
	ROTATION32X = 0x8  # size 4 (3 elements, order is determined with compress_bit_index)
	ROTATION20 = 0x9  # size 8 (1 element)
	ROTATION15 = 0xa  # size 6 (1 element)
	ROTATION10 = 0xb  # size 4 (1 element)
	ROTATION16 = 0xc  # size 2 (4 elements)


class KFMChannelTarget(Enum):
	Property = enum.auto()
	Scale = enum.auto()
	Translation = enum.auto()
	Rotation = enum.auto()


class MageFileType(Enum):
	Mesh = 1
	Node = 2
	Motion = 3
	Material = 4
	Twist = 5
	Collision = 6
	Name = 7
	ObjectInfo = 8
	PackInfo = 9
	ActorInfo = 10
