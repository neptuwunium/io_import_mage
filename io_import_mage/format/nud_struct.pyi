# SPDX-FileCopyrightText: 2026 Neptuwunium
#
# SPDX-License-Identifier: EUPL-1.2

from ctypes import BigEndianStructure

from io_import_mage.format.c3dmath import Vector3


class NUDBounds(BigEndianStructure):
	radius: float
	size: Vector3


class NUDShaderParamHeader(BigEndianStructure):
	next: int
	name_offset: int
	param_count: int
	reserved: int


class NUDTextureHeader(BigEndianStructure):
	global_index: int
	reserved: int
	reserved2: int
	attributes: int
	wrap_u: int
	wrap_v: int
	wrap_w: int
	mag: int
	min: int
	mip: int
	ansio: int
	reserved3: int
	bias: float


class NUDMaterialHeader(BigEndianStructure):
	global_index: int
	reserved: int
	attributes: int
	texture_count: int
	unknown1: int
	unknown2: int
	unknown3: int
	unknown4: int
	reserved2: int
	offset_scale: float
	offset_bias: float


class NUDPrimitiveHeader(BigEndianStructure):
	index_offset: int
	vertex_offset: int
	skin_vertex_offset: int
	vertex_count: int
	vertex_type: int
	material1_offset: int
	material2_offset: int
	material3_offset: int
	material4_offset: int
	face_count: int
	attributes: int
	unknown_1: int
	unknown_2: int
	unknown_3: int


class NUDObjectHeader(BigEndianStructure):
	bounds: NUDBounds
	bias: float
	offset: Vector3
	name_offset: int
	reserved1: int
	attributes: int
	mnt_index: int
	primitive_count: int
	primitive_offset: int


class NUDHeader(BigEndianStructure):
	magic: int
	size: int
	version_major: int
	version_minor: int
	object_count: int
	min_mnt_id: int
	max_mnt_id: int
	object_buffer_size: int
	index_buffer_size: int
	vertex_buffer_size: int
	skin_buffer_size: int
	bounds: NUDBounds
