# SPDX-FileCopyrightText: 2026 Neptuwunium
#
# SPDX-License-Identifier: EUPL-1.2

from typing import IO, Optional

import numpy as np
import numpy.typing as npt

from io_import_mage.format.structs.enums import KFMChannelTarget
from io_import_mage.format.structs.kfm_struct import *


class KFMNode:
	header: KFMNodeHeader
	values: npt.NDArray[np.float32]
	frames: npt.NDArray[np.int32]

	def __init__(self, stream: IO[bytes], frames: list[tuple[KFMFrame, IO[bytes], int]], index: int): pass


class KFMFile:
	valid: bool
	header: KFMHeader
	name: str
	nodes: dict[int, dict[KFMChannelTarget, KFMNode]]

	def __init__(self, stream: Optional[IO[bytes]]): pass
