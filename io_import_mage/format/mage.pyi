# SPDX-FileCopyrightText: 2026 Neptuwunium
#
# SPDX-License-Identifier: EUPL-1.2

from io import BytesIO
from types import TracebackType
from typing import Optional, IO

from .structs.enums import MageFileType


class MageFile:
	version: int
	is_big: bool
	name: Optional[str]
	game_id: int
	type_id: int
	count: int
	files: list[Optional[BytesIO]]
	offset_ranges: dict[MageFileType, tuple[int, int]]

	def __init__(self, stream: IO[bytes]): pass

	def __enter__(self) -> MageFile: pass

	def __exit__(
			self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
	) -> None: pass

	def get_file(self, file_type: MageFileType, index: int) -> Optional[BytesIO]: pass

	def get_count(self, file_type: MageFileType) -> int:

	def get_mesh(self, index: int) -> Optional[BytesIO]: pass

	def get_node(self, index: int) -> Optional[BytesIO]: pass

	def get_motion(self, index: int) -> Optional[BytesIO]: pass

	def get_material(self, index: int) -> Optional[BytesIO]: pass

	def get_twist(self, index: int) -> Optional[BytesIO]: pass

	def get_collision(self, index: int) -> Optional[BytesIO]: pass

	def get_name(self, index: int) -> Optional[BytesIO]: pass

	def get_object_info(self, index: int) -> Optional[BytesIO]: pass

	def get_pack_info(self, index: int) -> Optional[BytesIO]: pass

	def get_actor_info(self, index: int) -> Optional[BytesIO]: pass
