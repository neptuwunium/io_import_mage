# SPDX-FileCopyrightText: 2026 Neptuwunium
#
# SPDX-License-Identifier: EUPL-1.2

from ctypes import sizeof

from io_import_mage.format.structs.mnt_struct import *


class MNTNode:
	def __init__(self, stream, name):
		self.name = name
		self.header = MNTNodeHeader.from_buffer_copy(stream.read(sizeof(MNTNodeHeader)))


class MNTFile:
	def __init__(self, stream):
		self.valid = stream is not None
		if stream is None:
			return

		self.header = MNTHeader.from_buffer_copy(stream.read(sizeof(MNTHeader)))

		assert self.header.magic == 0x4D4E5400
		assert self.header.version_major == 1
		assert self.header.version_minor == 0

		self.nodes = []

		stream.seek(self.header.name_offset)
		string_buffer = stream.read().split(b'\x00')

		stream.seek(self.header.node_offset)
		for index in range(self.header.count):
			self.nodes.append(MNTNode(stream, string_buffer[index].decode('ascii')))


if __name__ == '__main__':
	import sys

	with open(sys.argv[1], 'rb') as f:
		if sys.argv[1].endswith('.mage'):
			from io_import_mage.format.mage import MageFile

			with MageFile(f) as mage_file:
				mnt_file = MNTFile(mage_file.get_node(0))
				print(mnt_file)
		else:
			mnt_file = MNTFile(f)
			print(mnt_file)
