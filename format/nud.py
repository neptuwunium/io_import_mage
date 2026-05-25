# SPDX-FileCopyrightText: 2026 Neptuwunium
#
# SPDX-License-Identifier: EUPL-1.2

import struct
from ctypes import sizeof
from enum import Enum

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
	def __init__(self, value):
		self.uv_count = value & 0xf
		self.uv_type = NUDVertexUVType((value >> 4) & 0xf)
		self.geometry_type = NUDVertexGeometryType((value >> 8) & 0xf)
		self.skin_type = NUDVertexSkinType((value >> 16) & 0xf)


class NUDShaderParam:
	def __init__(self, stream, string_buffer):
		self.header = NUDShaderParamHeader.from_buffer_copy(stream.read(sizeof(NUDShaderParamHeader)))
		self.name = string_buffer[self.header.name_offset:].split(b'\x00', 1)[0].decode('ascii')
		param_bytes = stream.read(4 * self.header.param_count)
		self.params_int = struct.unpack(f'>{self.header.param_count}I', param_bytes)
		self.params_float = struct.unpack(f'>{self.header.param_count}f', param_bytes)


class NUDTexture:
	def __init__(self, stream):
		self.header = NUDTextureHeader.from_buffer_copy(stream.read(sizeof(NUDTextureHeader)))


class NUDMaterial:
	def __init__(self, stream, string_buffer):
		self.header = NUDMaterialHeader.from_buffer_copy(stream.read(sizeof(NUDMaterialHeader)))
		self.textures = []
		self.params = []

		for _ in range(self.header.texture_count):
			self.textures.append(NUDTexture(stream))

		position = stream.tell()
		while True:
			stream.seek(position)
			param = NUDShaderParam(stream, string_buffer)
			self.params.append(param)
			if param.header.next == 0:
				break
			position = position + param.header.next


class NUDPrimitive:
	def __init__(self, stream, string_buffer):
		self.header = NUDPrimitiveHeader.from_buffer_copy(stream.read(sizeof(NUDPrimitiveHeader)))
		self.vertex_type = NUDVertexType(self.header.vertex_type)
		self.materials = [None] * 4

		if self.header.material1_offset > 0:
			stream.seek(self.header.material1_offset)
			self.materials[0] = NUDMaterial(stream, string_buffer)

		if self.header.material2_offset > 0:
			stream.seek(self.header.material2_offset)
			self.materials[1] = NUDMaterial(stream, string_buffer)

		if self.header.material3_offset > 0:
			stream.seek(self.header.material3_offset)
			self.materials[2] = NUDMaterial(stream, string_buffer)

		if self.header.material4_offset > 0:
			stream.seek(self.header.material4_offset)
			self.materials[3] = NUDMaterial(stream, string_buffer)


class NUDObject:
	def __init__(self, stream, string_buffer):
		self.header = NUDObjectHeader.from_buffer_copy(stream.read(sizeof(NUDObjectHeader)))
		self.name = string_buffer[self.header.name_offset:].split(b'\x00', 1)[0].decode('ascii')
		self.primitives = []

		for index in range(self.header.primitive_count):
			stream.seek(self.header.primitive_offset + sizeof(NUDPrimitiveHeader) * index)
			self.primitives.append(NUDPrimitive(stream, string_buffer))


class NUDFile:
	def __init__(self, stream):
		self.valid = stream is not None
		if stream is None:
			return

		self.header = NUDHeader.from_buffer_copy(stream.read(sizeof(NUDHeader)))

		assert self.header.magic == 0x4E445033
		assert self.header.version_major == 2
		assert self.header.version_minor == 0

		self.objects = []

		object_offset = stream.tell()

		stream.seek(object_offset + self.header.object_buffer_size)
		self.index_buffer = np.frombuffer(stream.read(self.header.index_buffer_size), dtype='>u2')
		self.vertex_buffer = np.frombuffer(stream.read(self.header.vertex_buffer_size), dtype='u1')
		self.skin_buffer = np.frombuffer(stream.read(self.header.skin_buffer_size), dtype='u1')
		string_buffer = stream.read()

		for index in range(self.header.object_count):
			stream.seek(object_offset + sizeof(NUDObjectHeader) * index)
			self.objects.append(NUDObject(stream, string_buffer))


if __name__ == '__main__':
	import sys

	with open(sys.argv[1], 'rb') as f:
		if sys.argv[1].endswith('.mage'):
			from format.mage import MageFile

			nud = NUDFile(MageFile(f).get_mesh(0))
		else:
			nud = NUDFile(f)
