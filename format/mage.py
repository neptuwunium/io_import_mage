# SPDX-FileCopyrightText: 2026 Neptuwunium
#
# SPDX-License-Identifier: EUPL-1.2

import sys
from enum import Enum
from io import BytesIO
from typing import Optional, IO
from struct import unpack

class MageFileType(Enum):
	Mesh = 1,
	Node = 2,
	Motion = 3,
	Material = 4,
	Twist = 5,
	Collision = 6,
	Name = 7,
	ObjectInfo = 8,
	PackInfo = 9,
	ActorInfo = 10,

class MageFile:
	version: int
	is_big: bool
	name: Optional[str]
	game_id: int
	type_id: int
	count: int
	files: list[Optional[BytesIO]]
	offset_ranges: dict[MageFileType, tuple[int, int]]

	OFFSET_RANGES = {
		0x0000: {
			MageFileType.Mesh      : (0, 1),
			MageFileType.Node      : (1, 1),
			MageFileType.Motion    : (2, 1),
			MageFileType.Material  : (3, 1),
			MageFileType.ObjectInfo: (4, 1),
			MageFileType.Twist     : (0, 0),
			MageFileType.Collision : (0, 0),
			MageFileType.Name      : (6, 1),
			MageFileType.PackInfo  : (7, 1),
			MageFileType.ActorInfo : (8, 1),
		},
		0x2000: {
			MageFileType.Mesh      : (0, 1),
			MageFileType.Node      : (1, 1),
			MageFileType.Motion    : (2, 1),
			MageFileType.Material  : (3, 1),
			MageFileType.ObjectInfo: (4, 1),
			MageFileType.Twist     : (0, 0),
			MageFileType.Collision : (0, 0),
			MageFileType.Name      : (7, 1),
			MageFileType.PackInfo  : (8, 1),
			MageFileType.ActorInfo : (9, 1),
		},
		0x0060: {
			MageFileType.Mesh      : (0, 2),
			MageFileType.Material  : (2, 1),
			MageFileType.ObjectInfo: (3, 2),
			MageFileType.Node      : (5, 1),
			MageFileType.Motion    : (6, 1),
			MageFileType.Name      : (7, 1),
			MageFileType.PackInfo  : (8, 1),
			MageFileType.ActorInfo : (9, 1),
			MageFileType.Collision : (0, 0),
			MageFileType.Twist     : (0, 0),
		},
		0x1000: {
			MageFileType.Mesh      : (0, 2),
			MageFileType.Material  : (2, 1),
			MageFileType.ObjectInfo: (3, 2),
			MageFileType.Node      : (5, 1),
			MageFileType.Motion    : (6, 1),
			MageFileType.Name      : (7, 1),
			MageFileType.PackInfo  : (8, 1),
			MageFileType.ActorInfo : (9, 1),
			MageFileType.Collision : (0, 0),
			MageFileType.Twist     : (0, 0),
		},
		0x0100: {
			MageFileType.Mesh      : (0, 2),
			MageFileType.Node      : (2, 2),
			MageFileType.Motion    : (4, 2),
			MageFileType.Material  : (6, 2),
			MageFileType.ObjectInfo: (8, 2),
			MageFileType.Collision : (10, 1),
			MageFileType.Name      : (12, 1),
			MageFileType.PackInfo  : (13, 1),
			MageFileType.ActorInfo : (14, 1),
			MageFileType.Twist     : (0, 0),
		},
		0x0200: {
			MageFileType.Mesh      : (0, 2),
			MageFileType.Node      : (2, 2),
			MageFileType.Motion    : (4, 2),
			MageFileType.Material  : (6, 2),
			MageFileType.ObjectInfo: (8, 2),
			MageFileType.Collision : (10, 1),
			MageFileType.Name      : (12, 1),
			MageFileType.PackInfo  : (13, 1),
			MageFileType.ActorInfo : (14, 1),
			MageFileType.Twist     : (0, 0),
		},
		0x0007: {
			MageFileType.Mesh      : (0, 12),
			MageFileType.ObjectInfo: (12, 8),
			MageFileType.Node      : (20, 1),
			MageFileType.Motion    : (21, 1),
			MageFileType.Collision : (22, 1),
			MageFileType.Name      : (23, 1),
			MageFileType.PackInfo  : (24, 1),
			MageFileType.ActorInfo : (25, 1),
			MageFileType.Material  : (0, 0),
			MageFileType.Twist     : (0, 0),
		},
		0x000a: {
			MageFileType.Mesh      : (0, 8),
			MageFileType.Node      : (8, 8),
			MageFileType.ObjectInfo: (16, 8),
			MageFileType.Material  : (24, 1),
			MageFileType.Motion    : (25, 1),
			MageFileType.Name      : (26, 1),
			MageFileType.PackInfo  : (27, 1),
			MageFileType.ActorInfo : (28, 1),
			MageFileType.Collision : (0, 0),
			MageFileType.Twist     : (0, 0),
		},
		0x0005: {
			MageFileType.Mesh      : (0, 16),
			MageFileType.Material  : (16, 8),
			MageFileType.ObjectInfo: (24, 16),
			MageFileType.Node      : (40, 2),
			MageFileType.Motion    : (42, 2),
			MageFileType.Collision : (44, 1),
			MageFileType.Twist     : (45, 1),
			MageFileType.Name      : (46, 1),
			MageFileType.PackInfo  : (47, 1),
			MageFileType.ActorInfo : (48, 1),
		},
		0x0009: {
			MageFileType.Mesh      : (0, 16),
			MageFileType.Material  : (16, 8),
			MageFileType.ObjectInfo: (24, 16),
			MageFileType.Node      : (40, 2),
			MageFileType.Motion    : (42, 2),
			MageFileType.Collision : (44, 1),
			MageFileType.Twist     : (45, 1),
			MageFileType.Name      : (46, 1),
			MageFileType.PackInfo  : (47, 1),
			MageFileType.ActorInfo : (48, 1),
		},
		0x0002: {
			MageFileType.Mesh      : (0, 11),
			MageFileType.Node      : (11, 11),
			MageFileType.Motion    : (22, 11),
			MageFileType.Material  : (33, 7),
			MageFileType.ObjectInfo: (40, 10),
			MageFileType.Collision : (51, 1),
			MageFileType.Name      : (52, 1),
			MageFileType.PackInfo  : (53, 1),
			MageFileType.ActorInfo : (54, 1),
			MageFileType.Twist     : (0, 0),
		},
		0x0003: {
			MageFileType.Mesh      : (0, 20),
			MageFileType.Material  : (20, 10),
			MageFileType.ObjectInfo: (30, 20),
			MageFileType.Node      : (50, 2),
			MageFileType.Motion    : (52, 2),
			MageFileType.Collision : (54, 1),
			MageFileType.Name      : (55, 1),
			MageFileType.PackInfo  : (56, 1),
			MageFileType.ActorInfo : (57, 1),
			MageFileType.Twist     : (0, 0),
		},
	}

	def __init__(self, stream: IO[bytes]):
		(magic, major, minor, patch, is_big, table_offset, count, _, type_id, game_id, name_length) = (
			unpack('=IBBB?iiiiIi', stream.read(0x20))
		)
		assert magic == 0x4547414D
		assert type_id in MageFile.OFFSET_RANGES

		self.version = major << 16 | minor << 8 | patch
		self.is_big = is_big
		self.game_id = game_id
		self.type_id = type_id
		self.count = count
		self.files = []
		self.offset_ranges = MageFile.OFFSET_RANGES[type_id]
		self.name = stream.read(name_length).decode('ascii') if name_length > 0 else None

		stream.seek(table_offset)

		for _ in range(count):
			(offset, size) = unpack('=ii', stream.read(0x8))
			if size > 0:
				next_entry = stream.tell()
				stream.seek(offset)
				self.files.append(BytesIO(stream.read(size)))
				stream.seek(next_entry)
			else:
				self.files.append(None)

	def get_file(self, file_type: MageFileType, index: int) -> Optional[BytesIO]:
		if file_type not in self.offset_ranges:
			return None

		(first_index, count) = self.offset_ranges[file_type]
		if count == 0 or index >= count:
			return None

		return self.files[first_index + index]

	def get_mesh(self, index: int) -> Optional[BytesIO]: return self.get_file(MageFileType.Mesh, index)
	def get_node(self, index: int) -> Optional[BytesIO]: return self.get_file(MageFileType.Node, index)
	def get_material(self, index: int) -> Optional[BytesIO]: return self.get_file(MageFileType.Material, index)
	def get_twist(self, index: int) -> Optional[BytesIO]: return self.get_file(MageFileType.Twist, index)
	def get_collision(self, index: int) -> Optional[BytesIO]: return self.get_file(MageFileType.Collision, index)
	def get_name(self, index: int) -> Optional[BytesIO]: return self.get_file(MageFileType.Name, index)
	def get_object_info(self, index: int) -> Optional[BytesIO]: return self.get_file(MageFileType.ObjectInfo, index)
	def get_pack_info(self, index: int) -> Optional[BytesIO]: return self.get_file(MageFileType.PackInfo, index)
	def get_actor_info(self, index: int) -> Optional[BytesIO]: return self.get_file(MageFileType.ActorInfo, index)

if __name__ == '__main__':
	with open(sys.argv[1], 'rb') as f:
		file = MageFile(f)