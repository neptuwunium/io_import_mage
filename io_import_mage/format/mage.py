# SPDX-FileCopyrightText: 2026 Neptuwunium
#
# SPDX-License-Identifier: EUPL-1.2

from ctypes import sizeof
from io import BytesIO

from io_import_mage.format.structs.enums import MageFileType
from io_import_mage.format.structs.mage_struct import *

OFFSET_RANGES = {
	0x0000: {
		MageFileType.Mesh: (0, 1),
		MageFileType.Node: (1, 1),
		MageFileType.Motion: (2, 1),
		MageFileType.Material: (3, 1),
		MageFileType.ObjectInfo: (4, 1),
		MageFileType.Twist: (0, 0),
		MageFileType.Collision: (0, 0),
		MageFileType.Name: (6, 1),
		MageFileType.PackInfo: (7, 1),
		MageFileType.ActorInfo: (8, 1),
	},
	0x2000: {
		MageFileType.Mesh: (0, 1),
		MageFileType.Node: (1, 1),
		MageFileType.Motion: (2, 1),
		MageFileType.Material: (3, 1),
		MageFileType.ObjectInfo: (4, 1),
		MageFileType.Twist: (0, 0),
		MageFileType.Collision: (0, 0),
		MageFileType.Name: (7, 1),
		MageFileType.PackInfo: (8, 1),
		MageFileType.ActorInfo: (9, 1),
	},
	0x0060: {
		MageFileType.Mesh: (0, 2),
		MageFileType.Material: (2, 1),
		MageFileType.ObjectInfo: (3, 2),
		MageFileType.Node: (5, 1),
		MageFileType.Motion: (6, 1),
		MageFileType.Name: (7, 1),
		MageFileType.PackInfo: (8, 1),
		MageFileType.ActorInfo: (9, 1),
		MageFileType.Collision: (0, 0),
		MageFileType.Twist: (0, 0),
	},
	0x1000: {
		MageFileType.Mesh: (0, 2),
		MageFileType.Material: (2, 1),
		MageFileType.ObjectInfo: (3, 2),
		MageFileType.Node: (5, 1),
		MageFileType.Motion: (6, 1),
		MageFileType.Name: (7, 1),
		MageFileType.PackInfo: (8, 1),
		MageFileType.ActorInfo: (9, 1),
		MageFileType.Collision: (0, 0),
		MageFileType.Twist: (0, 0),
	},
	0x0100: {
		MageFileType.Mesh: (0, 2),
		MageFileType.Node: (2, 2),
		MageFileType.Motion: (4, 2),
		MageFileType.Material: (6, 2),
		MageFileType.ObjectInfo: (8, 2),
		MageFileType.Collision: (10, 1),
		MageFileType.Name: (12, 1),
		MageFileType.PackInfo: (13, 1),
		MageFileType.ActorInfo: (14, 1),
		MageFileType.Twist: (0, 0),
	},
	0x0200: {
		MageFileType.Mesh: (0, 2),
		MageFileType.Node: (2, 2),
		MageFileType.Motion: (4, 2),
		MageFileType.Material: (6, 2),
		MageFileType.ObjectInfo: (8, 2),
		MageFileType.Collision: (10, 1),
		MageFileType.Name: (12, 1),
		MageFileType.PackInfo: (13, 1),
		MageFileType.ActorInfo: (14, 1),
		MageFileType.Twist: (0, 0),
	},
	0x0007: {
		MageFileType.Mesh: (0, 12),
		MageFileType.ObjectInfo: (12, 8),
		MageFileType.Node: (20, 1),
		MageFileType.Motion: (21, 1),
		MageFileType.Collision: (22, 1),
		MageFileType.Name: (23, 1),
		MageFileType.PackInfo: (24, 1),
		MageFileType.ActorInfo: (25, 1),
		MageFileType.Material: (0, 0),
		MageFileType.Twist: (0, 0),
	},
	0x000a: {
		MageFileType.Mesh: (0, 8),
		MageFileType.Material: (8, 8),
		MageFileType.ObjectInfo: (16, 8),
		MageFileType.Node: (24, 1),
		MageFileType.Motion: (25, 1),
		MageFileType.Name: (26, 1),
		MageFileType.PackInfo: (27, 1),
		MageFileType.ActorInfo: (28, 1),
		MageFileType.Collision: (0, 0),
		MageFileType.Twist: (0, 0),
	},
	0x0005: {
		MageFileType.Mesh: (0, 16),
		MageFileType.Material: (16, 8),
		MageFileType.ObjectInfo: (24, 16),
		MageFileType.Node: (40, 2),
		MageFileType.Motion: (42, 2),
		MageFileType.Collision: (44, 1),
		MageFileType.Twist: (45, 1),
		MageFileType.Name: (46, 1),
		MageFileType.PackInfo: (47, 1),
		MageFileType.ActorInfo: (48, 1),
	},
	0x0009: {
		MageFileType.Mesh: (0, 16),
		MageFileType.Material: (16, 8),
		MageFileType.ObjectInfo: (24, 16),
		MageFileType.Node: (40, 2),
		MageFileType.Motion: (42, 2),
		MageFileType.Collision: (44, 1),
		MageFileType.Twist: (45, 1),
		MageFileType.Name: (46, 1),
		MageFileType.PackInfo: (47, 1),
		MageFileType.ActorInfo: (48, 1),
	},
	0x0002: {
		MageFileType.Mesh: (0, 11),
		MageFileType.Node: (11, 11),
		MageFileType.Motion: (22, 11),
		MageFileType.Material: (33, 7),
		MageFileType.ObjectInfo: (40, 10),
		MageFileType.Collision: (51, 1),
		MageFileType.Name: (52, 1),
		MageFileType.PackInfo: (53, 1),
		MageFileType.ActorInfo: (54, 1),
		MageFileType.Twist: (0, 0),
	},
	0x0003: {
		MageFileType.Mesh: (0, 20),
		MageFileType.Material: (20, 10),
		MageFileType.ObjectInfo: (30, 20),
		MageFileType.Node: (50, 2),
		MageFileType.Motion: (52, 2),
		MageFileType.Collision: (54, 1),
		MageFileType.Name: (55, 1),
		MageFileType.PackInfo: (56, 1),
		MageFileType.ActorInfo: (57, 1),
		MageFileType.Twist: (0, 0),
	},
}


class MageFile:
	def __init__(self, stream):
		header = MAGEHeader.from_buffer_copy(stream.read(sizeof(MAGEHeader)))
		assert header.magic == 0x4547414D
		assert header.type_id in OFFSET_RANGES
		assert header.is_big

		self.version = header.version_major << 16 | header.version_minor << 8 | header.version_patch
		self.is_big = header.is_big
		self.game_id = header.game_id
		self.type_id = header.type_id
		self.count = header.count
		self.files = []
		self.offset_ranges = OFFSET_RANGES[self.type_id]
		self.name = stream.read(header.name_length).decode('ascii') if header.name_length > 0 else None

		stream.seek(header.table_offset)

		for _ in range(header.count):
			ptr = MAGEPtr.from_buffer_copy(stream.read(sizeof(MAGEPtr)))
			if ptr.size > 0:
				next_entry = stream.tell()
				stream.seek(ptr.offset)
				self.files.append(BytesIO(stream.read(ptr.size)))
				stream.seek(next_entry)
			else:
				self.files.append(None)

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		for tmp in self.files:
			if tmp is None: continue
			tmp.close()

	def get_file(self, file_type, index):
		if file_type not in self.offset_ranges:
			return None

		(first_index, count) = self.offset_ranges[file_type]
		if count == 0 or index >= count:
			return None

		file = self.files[first_index + index]
		if file is None:
			return None

		file.seek(0)
		return file

	def get_count(self, file_type):
		if file_type not in self.offset_ranges:
			return 0

		(_, count) = self.offset_ranges[file_type]
		return count

	def get_mesh(self, index):
		return self.get_file(MageFileType.Mesh, index)

	def get_node(self, index):
		return self.get_file(MageFileType.Node, index)

	def get_motion(self, index):
		return self.get_file(MageFileType.Motion, index)

	def get_material(self, index):
		return self.get_file(MageFileType.Material, index)

	def get_twist(self, index):
		return self.get_file(MageFileType.Twist, index)

	def get_collision(self, index):
		return self.get_file(MageFileType.Collision, index)

	def get_name(self, index):
		return self.get_file(MageFileType.Name, index)

	def get_object_info(self, index):
		return self.get_file(MageFileType.ObjectInfo, index)

	def get_pack_info(self, index):
		return self.get_file(MageFileType.PackInfo, index)

	def get_actor_info(self, index):
		return self.get_file(MageFileType.ActorInfo, index)


if __name__ == '__main__':
	import sys

	with open(sys.argv[1], 'rb') as f:
		with MageFile(f) as mage_file:
			print(mage_file)
