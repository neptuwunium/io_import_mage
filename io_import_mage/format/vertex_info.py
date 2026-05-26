# SPDX-FileCopyrightText: 2026 Neptuwunium
#
# SPDX-License-Identifier: EUPL-1.2

from enum import Enum


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
	I4W32 = 0x1


class NUDVertexUVType(Enum):
	U16 = 0x0
	U32 = 0x1
	C8U16 = 0x2
	C8U32 = 0x3
	C16U16 = 0x4
	C16U32 = 0x5


class VertexStorageType(Enum):
	RGBA8_UNORM = 0,
	RG32_FLOAT = 1,
	RGB32_FLOAT = 2,
	RGBA32_FLOAT = 3,
	RG16_FLOAT = 4,
	RGB16_FLOAT = 5,
	RGBA16_FLOAT = 6,
	RGBA32_INT = 7,


class VertexSemanticType(Enum):
	Position = 0
	Normal = 1
	Binormal = 2
	Tangent = 3
	Color = 4
	UV = 5
	BoneIndex = 6
	BoneWeight = 7


class VertexSemantic:
	offset: int
	storage: VertexStorageType
	type: VertexSemanticType
	index: int

	def __init__(self, offset: int, storage: VertexStorageType, vtype: VertexSemanticType, index: int = 0):
		self.offset = offset
		self.storage = storage
		self.type = vtype
		self.index = index


class VertexInfo:
	stride: int
	elements: list[VertexSemantic]

	def __init__(self, stride: int, elements: list[VertexSemantic]):
		self.stride = stride
		self.elements = elements


# table dumped from ACAH and adjusted for what we can import
VERTEX_INFO = {
	NUDVertexGeometryType.P32: VertexInfo(
		0x10,
		[
			VertexSemantic(0x0, VertexStorageType.RGBA32_FLOAT, VertexSemanticType.Position),
		]
	),
	NUDVertexGeometryType.P32N32: VertexInfo(
		0x20,
		[
			VertexSemantic(0x0, VertexStorageType.RGBA32_FLOAT, VertexSemanticType.Position),
			VertexSemantic(0x10, VertexStorageType.RGB32_FLOAT, VertexSemanticType.Normal),
		]
	),
	NUDVertexGeometryType.P32NB32: VertexInfo(
		0x30,
		[
			VertexSemantic(0x0, VertexStorageType.RGBA32_FLOAT, VertexSemanticType.Position),
			VertexSemantic(0x10, VertexStorageType.RGBA32_FLOAT, VertexSemanticType.Normal),
			VertexSemantic(0x20, VertexStorageType.RGBA32_FLOAT, VertexSemanticType.Binormal),
		]
	),
	NUDVertexGeometryType.P32NBT32: VertexInfo(
		0x40,
		[
			VertexSemantic(0x0, VertexStorageType.RGBA32_FLOAT, VertexSemanticType.Position),
			VertexSemantic(0x10, VertexStorageType.RGBA32_FLOAT, VertexSemanticType.Normal),
			VertexSemantic(0x20, VertexStorageType.RGBA32_FLOAT, VertexSemanticType.Binormal),
			VertexSemantic(0x30, VertexStorageType.RGBA32_FLOAT, VertexSemanticType.Tangent),
		]
	),
	# todo: N11/NBT11 is R11G11B10 (i think) but this is ass to implement in numpy
	NUDVertexGeometryType.P32N11: VertexInfo(
		0x10,
		[
			VertexSemantic(0x0, VertexStorageType.RGB32_FLOAT, VertexSemanticType.Position),
			VertexSemantic(0xc, VertexStorageType.RGBA8_UNORM, VertexSemanticType.Normal),
		]
	),
	NUDVertexGeometryType.P32NBT11: VertexInfo(
		0x18,
		[
			VertexSemantic(0x0, VertexStorageType.RGB32_FLOAT, VertexSemanticType.Position),
			VertexSemantic(0xc, VertexStorageType.RGBA8_UNORM, VertexSemanticType.Normal),
			VertexSemantic(0x10, VertexStorageType.RGBA8_UNORM, VertexSemanticType.Binormal),
			VertexSemantic(0x14, VertexStorageType.RGBA8_UNORM, VertexSemanticType.Tangent),
		]
	),
	NUDVertexGeometryType.P32N16: VertexInfo(
		0x14,
		[
			VertexSemantic(0x0, VertexStorageType.RGB32_FLOAT, VertexSemanticType.Position),
			VertexSemantic(0xc, VertexStorageType.RGB16_FLOAT, VertexSemanticType.Normal),
		]
	),
	NUDVertexGeometryType.P32NBT16: VertexInfo(
		0x24,
		[
			VertexSemantic(0x0, VertexStorageType.RGB32_FLOAT, VertexSemanticType.Position),
			VertexSemantic(0xc, VertexStorageType.RGB16_FLOAT, VertexSemanticType.Normal),
			VertexSemantic(0x14, VertexStorageType.RGB16_FLOAT, VertexSemanticType.Binormal),
			VertexSemantic(0x1c, VertexStorageType.RGB16_FLOAT, VertexSemanticType.Tangent),
		]
	),
	NUDVertexGeometryType.P16N16: VertexInfo(
		0x10,
		[
			VertexSemantic(0x0, VertexStorageType.RGB16_FLOAT, VertexSemanticType.Position),
			VertexSemantic(0x8, VertexStorageType.RGB16_FLOAT, VertexSemanticType.Normal),
		]
	),
	NUDVertexUVType.U16: VertexInfo(
		0x4,
		[
			VertexSemantic(0x0, VertexStorageType.RG16_FLOAT, VertexSemanticType.UV),
		]
	),
	NUDVertexUVType.U32: VertexInfo(
		0x8,
		[
			VertexSemantic(0x0, VertexStorageType.RG32_FLOAT, VertexSemanticType.UV),
		]
	),
	NUDVertexUVType.C8U16: VertexInfo(
		0x8,
		[
			VertexSemantic(0x0, VertexStorageType.RGBA8_UNORM, VertexSemanticType.Color),
			VertexSemantic(0x4, VertexStorageType.RG16_FLOAT, VertexSemanticType.UV),
		]
	),
	NUDVertexUVType.C8U32: VertexInfo(
		0xc,
		[
			VertexSemantic(0x0, VertexStorageType.RGBA8_UNORM, VertexSemanticType.Color),
			VertexSemantic(0x4, VertexStorageType.RG32_FLOAT, VertexSemanticType.UV),
		]
	),
	NUDVertexUVType.C16U16: VertexInfo(
		0xc,
		[
			VertexSemantic(0x0, VertexStorageType.RGBA16_FLOAT, VertexSemanticType.Color),
			VertexSemantic(0x8, VertexStorageType.RG16_FLOAT, VertexSemanticType.UV),
		]
	),
	NUDVertexUVType.C16U32: VertexInfo(
		0x10,
		[
			VertexSemantic(0x0, VertexStorageType.RGBA16_FLOAT, VertexSemanticType.Color),
			VertexSemantic(0x8, VertexStorageType.RG32_FLOAT, VertexSemanticType.UV),
		]
	),
	NUDVertexSkinType.I0: VertexInfo(
		0x0, []
	),
	NUDVertexSkinType.I4W32: VertexInfo(
		0x20,
		[
			VertexSemantic(0x0, VertexStorageType.RGBA32_INT, VertexSemanticType.BoneIndex),
			VertexSemantic(0x10, VertexStorageType.RGBA32_FLOAT, VertexSemanticType.BoneWeight),
		]
	),
}


# uv is color + uv * n
def get_uv_info(info: VertexInfo, count: int) -> VertexInfo:
	if count == 1:
		return info

	stride = info.stride
	base = 0
	elements = []
	if len(info.elements) > 1:
		base = info.elements[1].offset
		stride -= base
		elements.append(info.elements[0])
	size = stride
	stride *= count

	offset = base
	for index in range(count):
		elements.append(VertexSemantic(offset, info.elements[-1].storage, info.elements[-1].type, index=index))
		offset += size
	return VertexInfo(stride + base, elements)
