# SPDX-FileCopyrightText: 2026 Neptuwunium
#
# SPDX-License-Identifier: EUPL-1.2

import struct
from ctypes import sizeof
from io import BytesIO

from io_import_mage.format.kfm import KFMFile
from io_import_mage.format.structs.mop_struct import *


class MOPFile:
	def __init__(self, stream):
		self.valid = stream is not None
		if stream is None:
			return

		self.header = MOPHeader.from_buffer_copy(stream.read(sizeof(MOPHeader)))
		self.animations = {}

		assert self.header.magic == 0x4D4F5032
		assert self.header.version_major == 1
		assert self.header.version_minor == 2

		if self.header.count == 0:
			return

		stream.seek(self.header.size_offset)
		sizes = struct.unpack(f'>{self.header.count}I', stream.read(4 * self.header.count))

		stream.seek(self.header.anim_offset)
		offsets = struct.unpack(f'>{self.header.count}I', stream.read(4 * self.header.count))

		stream.seek(self.header.name_offset)
		name_offsets = struct.unpack(f'>{self.header.count}I', stream.read(4 * self.header.count))

		stream.seek(0)
		string_buffer = stream.read(offsets[0])  # this should be header_size, but it's bugged!

		for (size, offset, name_offset) in zip(sizes, offsets, name_offsets):
			stream.seek(name_offset)
			name = string_buffer[name_offset:].split(b'\x00')[0].decode('ascii')
			stream.seek(offset)
			self.animations[name] = BytesIO(stream.read(size))

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		for anim in self.animations.values():
			anim.close()

	def load(self, name):
		if name not in self.animations:
			return None

		return KFMFile(self.animations[name])


if __name__ == '__main__':
	import sys

	with open(sys.argv[1], 'rb') as f:
		if sys.argv[1].endswith('.mage'):
			from io_import_mage.format.mage import MageFile

			with MageFile(f) as mage_file:
				with MOPFile(mage_file.get_motion(0)) as mop_file:
					print(mop_file)
		else:
			with MOPFile(f) as mop_file:
				print(mop_file)
