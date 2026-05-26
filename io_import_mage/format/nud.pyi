# SPDX-FileCopyrightText: 2026 Neptuwunium
#
# SPDX-License-Identifier: EUPL-1.2

from typing import Optional, IO

import numpy as np
import numpy.typing as npt

from io_import_mage.format.structs.nud_struct import *
from io_import_mage.format.vertex_info import *


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
	unique_id: int

	def __init__(self, stream: IO[bytes], string_buffer: bytes): pass


class NUDVertexStream:
	position: npt.NDArray
	normal: Optional[npt.NDArray]
	color: Optional[npt.NDArray]
	uv: list[npt.NDArray]

	def __init__(self, nud: NUDFile, prim: NUDPrimitive): pass


class NUDTriangleStream:
	triangles: npt.NDArray

	def __init__(self, nud: NUDFile, prim: NUDPrimitive): pass


class NUDSkinVertexStream:
	indices: npt.NDArray[np.int16]
	weights: npt.NDArray[np.float32]

	def __init__(self, nud: NUDFile, prim: NUDPrimitive) -> Optional[NUDSkinVertexStream]: pass


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
	index_buffer: npt.NDArray[np.uint16]
	vertex_buffer: npt.NDArray[np.uint8]
	skin_buffer: npt.NDArray[np.uint8]

	def __init__(self, stream: Optional[IO[bytes]]): pass
