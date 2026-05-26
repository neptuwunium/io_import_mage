# SPDX-FileCopyrightText: 2026 Neptuwunium
#
# SPDX-License-Identifier: EUPL-1.2

from io import BytesIO
from types import TracebackType
from typing import IO, Optional

from io_import_mage.format.structs.mop_struct import *
from io_import_mage.format.kfm import KFMFile


class MOPFile:
	valid: bool
	header: MOPHeader
	animations: dict[str, BytesIO]

	def __init__(self, stream: Optional[IO[bytes]]): pass

	def __enter__(self) -> MOPFile: pass

	def __exit__(
			self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
	) -> None: pass

	def load(self, name: str) -> Optional[KFMFile]: pass