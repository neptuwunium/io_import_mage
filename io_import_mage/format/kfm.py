# SPDX-FileCopyrightText: 2026 Neptuwunium
#
# SPDX-License-Identifier: EUPL-1.2

from ctypes import sizeof

from io_import_mage.format.structs.kfm_struct import *


class KFMFile:
	def __init__(self, stream):
		self.valid = stream is not None
		if stream is None:
			return

		self.header = KFMHeader.from_buffer_copy(stream.read(sizeof(KFMHeader)))

		assert self.header.magic == 0x4B464D31
		assert self.header.version_major == 2
		assert self.header.version_minor == 3

		# todo


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
