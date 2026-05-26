# SPDX-FileCopyrightText: 2026 Neptuwunium
#
# SPDX-License-Identifier: EUPL-1.2

from ctypes import BigEndianStructure, c_uint, c_byte, c_ushort, c_int, c_float, c_short

from io_import_mage.format.c3dmath import Vector3


class NUDBounds(BigEndianStructure):
	_pack_ = 4
	_fields_ = [
		('radius', c_float),
		('position', Vector3),
	]


class NUDShaderParamHeader(BigEndianStructure):
	_pack_ = 1
	_fields_ = [
		('next', c_int),
		('name_offset', c_int),
		('param_count', c_int),
		('reserved', c_int),
	]


class NUDTextureHeader(BigEndianStructure):
	_pack_ = 1
	_fields_ = [
		('global_index', c_int),
		('reserved', c_int),
		('reserved2', c_ushort),
		('attributes', c_ushort),
		('wrap_u', c_byte),
		('wrap_v', c_byte),
		('wrap_w', c_byte),
		('mag', c_byte),
		('min', c_byte),
		('mip', c_byte),
		('ansio', c_byte),
		('reserved3', c_byte),
		('bias', c_float),
	]


class NUDMaterialHeader(BigEndianStructure):
	_pack_ = 1
	_fields_ = [
		('global_index', c_int),
		('reserved', c_int),
		('attributes', c_ushort),
		('texture_count', c_ushort),
		('alpha_blend', c_ushort),
		('alpha_test_func', c_ushort),
		('alpha_test_ref', c_ushort),
		('cull_mode', c_ushort),
		('reserved2', c_int),
		('offset_scale', c_float),
		('offset_bias', c_float),
	]


class NUDPrimitiveHeader(BigEndianStructure):
	_pack_ = 1
	_fields_ = [
		('index_offset', c_int),
		('vertex_offset', c_int),
		('skin_vertex_offset', c_int),
		('vertex_count', c_ushort),
		('vertex_type', c_ushort),
		('material1_offset', c_int),
		('material2_offset', c_int),
		('material3_offset', c_int),
		('material4_offset', c_int),
		('face_count', c_ushort),
		('attributes', c_ushort),
		('unknown_1', c_int),
		('unknown_2', c_int),
		('unknown_3', c_int),
	]


class NUDObjectHeader(BigEndianStructure):
	_pack_ = 1
	_fields_ = [
		('bounds', NUDBounds),
		('offset', Vector3),
		('bias', c_float),
		('name_offset', c_int),
		('reserved1', c_short),
		('attributes', c_ushort),
		('mnt_index', c_ushort),
		('primitive_count', c_ushort),
		('primitive_offset', c_int),
	]


class NUDHeader(BigEndianStructure):
	_pack_ = 1
	_fields_ = [
		('magic', c_uint),
		('size', c_uint),
		('version_major', c_byte),
		('version_minor', c_byte),
		('object_count', c_ushort),
		('min_mnt_id', c_ushort),
		('max_mnt_id', c_ushort),
		('object_buffer_size', c_int),
		('index_buffer_size', c_int),
		('vertex_buffer_size', c_int),
		('skin_buffer_size', c_int),
		('bounds', NUDBounds),
	]
