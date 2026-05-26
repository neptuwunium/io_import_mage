# SPDX-FileCopyrightText: 2026 Neptuwunium
#
# SPDX-License-Identifier: EUPL-1.2

import struct
from ctypes import sizeof
from io import BytesIO

import numpy as np

from io_import_mage.format.structs.enums import KFMChannelStorage
from io_import_mage.format.structs.kfm_struct import *


class KFMNode:
	def __init__(self, stream, frames, index):
		self.header = KFMNodeHeader.from_buffer_copy(stream.read(sizeof(KFMNodeHeader)))

		# noinspection PyTypeChecker
		self.values = np.empty((0, self.header.count), dtype=np.float32)
		# noinspection PyTypeChecker
		self.frames = np.empty((0, 1), dtype=np.int32)

		values = []
		frame_ids = []
		for (frame_header, frame, frame_start) in frames:
			frame.seek(sizeof(KFMFrame) + index * sizeof(KFMFrameNode))
			frame_node_header = KFMFrameNode.from_buffer_copy(frame.read(sizeof(KFMFrameNode)))

			frame.seek(frame_header.frame_offset + frame_node_header.frame_id_index * 2)
			ids = struct.unpack(f'>{frame_node_header.frame_count}H', frame.read(2 * frame_node_header.frame_count))

			frame.seek(frame_node_header.value_offset)
			for frame_index in range(frame_node_header.frame_count):
				frame_ids.append(ids[frame_index] + frame_start)
				for _ in range(self.header.count):
					match self.header.channel:
						case KFMChannelStorage.ROTATION_RADIANS:
							return  # todo
						case KFMChannelStorage.ROTATION32X:
							return  # todo
						case KFMChannelStorage.ROTATION20:
							return  # todo
						case KFMChannelStorage.ROTATION15:
							return  # todo
						case KFMChannelStorage.ROTATION10:
							return  # todo
						case KFMChannelStorage.ROTATION16:
							values.append(struct.unpack('>e', frame.read(4))[0])
						case _:
							values.append(struct.unpack('>f', frame.read(4))[0])

		# noinspection PyTypeChecker
		self.values = np.array(values).reshape(-1, self.header.count)
		# noinspection PyTypeChecker
		self.frames = frame_ids


class KFMFile:
	def __init__(self, stream):
		self.valid = stream is not None
		if stream is None:
			return

		self.header = KFMHeader.from_buffer_copy(stream.read(sizeof(KFMHeader)))

		assert self.header.magic == 0x4B464D31
		assert self.header.version_major == 2
		assert self.header.version_minor == 3
		assert self.header.frame_info_count >= 2

		stream.seek(self.header.name_offset)
		self.name = stream.read(self.header.file_size - self.header.name_offset).split(b'\x00', 1)[0].decode('ascii')

		frames = []
		for index in range(self.header.frame_info_count):
			stream.seek(self.header.frame_count_offset + index * 2)
			frame_index = struct.unpack('>H', stream.read(2))[0]
			stream.seek(self.header.frame_info_offset + index * sizeof(KFMPtr))
			ptr = KFMPtr.from_buffer_copy(stream.read(sizeof(KFMPtr)))
			stream.seek(ptr.offset)
			frame_buffer = BytesIO(stream.read(ptr.size))
			frame_header = KFMFrame.from_buffer_copy(frame_buffer.read(sizeof(KFMFrame)))
			frames.append((frame_header, frame_buffer, frame_index))

		self.nodes = {}
		stream.seek(self.header.node_offset)

		# const only has one frame list
		for index in range(self.header.const_count):
			node = KFMNode(stream, [frames[0]], index)
			if node.header.mnt_id not in self.nodes:
				self.nodes[node.header.mnt_id] = {}
			self.nodes[node.header.mnt_id][node.header.target] = node

		# motion uses the rest
		for index in range(self.header.motion_count):
			node = KFMNode(stream, frames[1:], index)
			if node.header.mnt_id not in self.nodes:
				self.nodes[node.header.mnt_id] = {}
			self.nodes[node.header.mnt_id][node.header.target] = node


if __name__ == '__main__':
	import sys
	from io_import_mage.format import MOPFile

	with open(sys.argv[1], 'rb') as f:
		if sys.argv[1].endswith('.mage'):
			from io_import_mage.format.mage import MageFile

			with MageFile(f) as mage_file:
				with MOPFile(mage_file.get_motion(0)) as mop_file:
					kfm_file = mop_file.load('basepose')
					print(kfm_file)
		elif sys.argv[1].endswith('.mop'):
			with MOPFile(f) as mop_file:
				kfm_file = mop_file.load('basepose')
				print(kfm_file)
		else:
			kfm_file = KFMFile(f)
			print(kfm_file)
