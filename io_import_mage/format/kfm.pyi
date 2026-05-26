# SPDX-FileCopyrightText: 2026 Neptuwunium
#
# SPDX-License-Identifier: EUPL-1.2

from typing import IO, Optional

from io_import_mage.format.structs.kfm_struct import *


class KFMFile:
	valid: bool
	header: KFMHeader

	def __init__(self, stream: Optional[IO[bytes]]): pass
