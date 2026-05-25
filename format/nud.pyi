# SPDX-FileCopyrightText: 2026 Neptuwunium
#
# SPDX-License-Identifier: EUPL-1.2

from enum import Enum
from typing import Optional, IO

import numpy as np

from format.nud_struct import *


class NUDVertexGeometryType(Enum):
	P32 = 0x0
	P32N32 = 0x1
	P32NB32 = 0x2
	P32NBT32 = 0x3
	P32N11 = 0x4
	P32NBT11 = 0x5
	P32N16 = 0x6
	P32NBT16 = 0x7
	P16N16 = 0x8


class NUDVertexSkinType(Enum):
	I0 = 0x0
	I4W16 = 0x1
	I4W32 = 0x2
	I8W16 = 0x3
	I8W32 = 0x4


class NUDVertexUVType(Enum):
	U16 = 0x0
	U32 = 0x1
	C8U16 = 0x2
	C8U32 = 0x3
	C16U16 = 0x4
	C16U32 = 0x5


class NUDVertexType:
	geometry_type: NUDVertexGeometryType
	skin_type: NUDVertexSkinType
	uv_type: NUDVertexUVType
	uv_count: int

	def __init__(self, value: int): pass


class NUDTexture:
	header: NUDTextureHeader

	def __init__(self, stream: IO[bytes]): pass


class NUDShaderParam:
	header: NUDShaderParamHeader
	name: str
	params_float: tuple[float, ...]
	params_int: tuple[int, ...]

	def __init__(self, stream: IO[bytes], string_buffer: bytes): pass


class NUDMaterial:
	header: NUDMaterialHeader
	textures: list[NUDTexture]
	params: list[NUDShaderParam]

	def __init__(self, stream: IO[bytes], string_buffer: bytes): pass


class NUDPrimitive:
	header: NUDPrimitiveHeader
	materials: list[Optional[NUDMaterial]]
	vertex_type: NUDVertexType

	def __init__(self, stream: IO[bytes], string_buffer: bytes): pass


class NUDObject:
	header: NUDObjectHeader
	name: str
	primitives: list[NUDPrimitive]

	def __init__(self, stream: IO[bytes], string_buffer: bytes): pass


class NUDFile:
	valid: bool
	header: NUDHeader
	objects: list[NUDObject]
	index_buffer: np.typing.NDArray[np.uint16]
	vertex_buffer: np.typing.NDArray[np.uint8]
	skin_buffer: np.typing.NDArray[np.uint8]

	def __init__(self, stream: Optional[IO[bytes]]): pass
