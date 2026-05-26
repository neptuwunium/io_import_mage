# SPDX-FileCopyrightText: 2026 Neptuwunium
#
# SPDX-License-Identifier: EUPL-1.2

from typing import Optional, IO

from io_import_mage.format.structs.mnt_struct import *


class MNTNode:
	header: MNTNodeHeader
	name: str

	def __init__(self, stream: IO[bytes], name: str): pass


class MNTFile:
	valid: bool
	header: MNTHeader
	nodes: list[MNTNode]

	def __init__(self, stream: Optional[IO[bytes]]): pass
