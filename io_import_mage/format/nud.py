# SPDX-FileCopyrightText: 2026 Neptuwunium
#
# SPDX-License-Identifier: EUPL-1.2

import struct
from ctypes import sizeof

import numpy as np

from io_import_mage.format.nud_struct import *
from io_import_mage.format.vertex_info import NUDVertexUVType, NUDVertexGeometryType, NUDVertexSkinType, \
	VertexStorageType, \
	VertexSemanticType
from . import vertex_info


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


def mmhmix(h: int, k: int) -> int:
	k = (k * 0xcc9e2d51) & 0xffffffff
	k = ((k << 15) | (k >> 17)) & 0xffffffff
	k = (k * 0x1b873593) & 0xffffffff
	h ^= k
	h = ((h << 13) | (h >> 19)) & 0xffffffff
	h = (h * 5 + 0xe6546b64) & 0xffffffff
	return h


class NUDMaterial:
	def __init__(self, stream, string_buffer):
		self.header = NUDMaterialHeader.from_buffer_copy(stream.read(sizeof(NUDMaterialHeader)))
		self.textures = []
		self.params = []
		self.unique_id = self.header.global_index

		for _ in range(self.header.texture_count):
			self.textures.append(NUDTexture(stream))
			self.unique_id = mmhmix(self.unique_id, self.textures[-1].header.global_index)

		position = stream.tell()
		while True:
			stream.seek(position)
			param = NUDShaderParam(stream, string_buffer)
			self.params.append(param)
			for item in param.params_int:
				self.unique_id = mmhmix(self.unique_id, item)
			if param.header.next == 0:
				break
			position = position + param.header.next


STORAGE_TO_NUMPY = {
	VertexStorageType.RGBA8_UNORM: '>4u1',
	VertexStorageType.RG32_FLOAT: '>2f4',
	VertexStorageType.RGB32_FLOAT: '>3f4',
	VertexStorageType.RGBA32_FLOAT: '>4f4',
	VertexStorageType.RG16_FLOAT: '>2f2',
	VertexStorageType.RGB16_FLOAT: '>3f2',
	VertexStorageType.RGBA16_FLOAT: '>4f2',
	VertexStorageType.RGBA16_INT: '>4u2',
}


# 16-bit or unorm to 32-bit
def unwrap(array: np.typing.NDArray, storage: VertexStorageType) -> np.typing.NDArray:
	match storage:
		case VertexStorageType.RGBA8_UNORM:
			return array / 255.0
		case VertexStorageType.RG16_FLOAT:
			return array.astype(np.float32)
		case VertexStorageType.RGB16_FLOAT:
			return array.astype(np.float32)
		case VertexStorageType.RGBA16_FLOAT:
			return array.astype(np.float32)
		case VertexStorageType.RGBA16_INT:
			return array.astype(np.int32)
		case _:
			return array


# todo: copy this for NUDSkinVertexStream, but need to construct the armature first from MOP and MNT :)
class NUDVertexStream:
	def __init__(self, nud, prim):
		geo_info = vertex_info.VERTEX_INFO[prim.vertex_type.geometry_type]
		uv_info = vertex_info.get_uv_info(vertex_info.VERTEX_INFO[prim.vertex_type.uv_type], prim.vertex_type.uv_count)
		total_stride = geo_info.stride + uv_info.stride

		vertex_start = prim.header.vertex_offset
		vertex_count = prim.header.vertex_count
		vertex_end = vertex_start + vertex_count * total_stride

		names = []
		semantic_idx = []
		formats = []
		offsets = []

		for element in geo_info.elements:
			semantic = element.type
			storage = element.storage
			names.append(semantic.name)
			formats.append(STORAGE_TO_NUMPY[storage])
			offsets.append(element.offset)
			semantic_idx.append(element)

		for element in uv_info.elements:
			semantic = element.type
			storage = element.storage
			names.append(f'{semantic.name}{element.index}' if element.index > 0 else semantic.name)
			formats.append(STORAGE_TO_NUMPY[storage])
			offsets.append(element.offset + geo_info.stride)
			semantic_idx.append(element)

		view = np.frombuffer(nud.vertex_buffer[vertex_start:vertex_end], dtype={
			'names': names,
			'formats': formats,
			'offsets': offsets,
			'itemsize': total_stride
		})

		self.normal = None
		self.color = None

		# noinspection PyTypeChecker
		# reasoning: set to not null
		self.uv = [None] * prim.vertex_type.uv_count
		for index in range(len(semantic_idx)):
			semantic = semantic_idx[index]
			match semantic.type:
				case VertexSemanticType.Position:
					self.position = unwrap(view[names[index]].copy(), semantic.storage)
				case VertexSemanticType.Normal:
					self.normal = unwrap(view[names[index]].copy(), semantic.storage)
				case VertexSemanticType.Color:
					self.color = unwrap(view[names[index]].copy(), semantic.storage)
				case VertexSemanticType.UV:
					uv = unwrap(view[names[index]].copy(), semantic.storage)
					uv[:, 1] = 1.0 - uv[:, 1]
					self.uv[semantic.index] = uv


class NUDTriangleStream:
	def __init__(self, nud, prim):
		index_start = prim.header.index_offset // 2
		index_end = index_start + prim.header.face_count
		indices = nud.index_buffer[index_start:index_end]
		restart = np.where(indices == 0xFFFF)[0]
		strips = np.split(indices, restart)

		triangles = []
		for strip in strips:
			if len(strip) > 0 and strip[0] == 0xFFFF:
				strip = strip[1:]

			if len(strip) < 3:
				continue

			t0 = strip[:-2]
			t1 = strip[1:-1]
			t2 = strip[2:]

			tris = np.column_stack((t0, t1, t2))
			tris[1::2, [0, 1]] = tris[1::2, [1, 0]]

			degen_mask = (t0 != t1) & (t1 != t2) & (t0 != t2)
			triangles.append(tris[degen_mask])

		# noinspection PyTypeChecker
		# reasoning: complex type
		self.triangles = np.empty((0, 3), dtype=np.uint16) if not triangles else np.vstack(triangles)


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
			from io_import_mage.format.mage import MageFile

			nud_file = NUDFile(MageFile(f).get_mesh(0))
		else:
			nud_file = NUDFile(f)

		vert = NUDVertexStream(nud_file, nud_file.objects[0].primitives[0])
		tri = NUDTriangleStream(nud_file, nud_file.objects[0].primitives[0])
